# Ava auto-smart
from __future__ import with_statement
from __future__ import absolute_import
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import webbrowser
import os
import avanlp
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
import sys
import re
from six.moves import queue
import hashlib
import asearch
"""Synthesizes speech from the input string of text."""
from google.cloud import texttospeech

avaCasual = False
nlpEnabled = True

# [END import_libraries]

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]


def listen_print_loop(responses):
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
    is provided by the server.
    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.
    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        response.results[0]

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()
            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            for names in ava:
                index = transcript.lower().find(names)
                if index != -1:
                    print(transcript.lower()[index+4:])
                    if nlpEnabled:
                        process(transcript.lower()[index+4:])
                    else:
                        say(asearch.ddg(transcript.lower()[index+4:]))
                elif avaCasual:
                    print("Casual: " + transcript.lower())
                    process(transcript.lower())

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag
    recog = enums.RecognitionConfig
    enums.RecognitionConfig.AudioEncoding.LINEAR16
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        speech_contexts=[types.SpeechContext(
            phrases=ava,
        )])
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        while 1:
            try:
                # Now, put the transcription responses to use.
                listen_print_loop(responses)
            except Exception as e:
                print "Restarting"
                print e
                main()


# Defining variables
ava = ['eva', 'ava', 'evil', 'ada']

# Text to speech


def say(words):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=words)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    print "Ava: " + words
    hash = hashlib.md5(''.join(e for e in words if e.isalnum())[
                       0:254].lower()).hexdigest()
    speech_filename = './tts/' + hash + '.mp3'.lower()
    # The response's audio_content is binary.
    if not os.path.isfile(speech_filename):
        with open(speech_filename, 'wb') as out:
            out.write(response.audio_content)
    if os.path.isfile(speech_filename):
        playsound(speech_filename)


def process(command):
    # Obtaining global variables
    global usrinput

    # Setting user input
    usrinput = command

    print usrinput

    print 'Test'
    # Playing activated sound
    if 'exit' in usrinput:
        playsound("./audio/exit.mp3")
        exit()
    else:
        playsound("./audio/activation.mp3")

    # Displaying user input
    print "You: " + usrinput

    # Getting response from usedr input
    if usrinput != '':
        say(avanlp.respond(usrinput))


# Open simple ui
# bwebbrowser.open('file://' + os.path.realpath('gui/gui.html'))

main()
