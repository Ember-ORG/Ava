from __future__ import absolute_import
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re

# Initializing global variables
usrsentences = []
filtered_sentence = []
response = ''

# Word dictionary
question = ['what', 'where', 'why', 'how', 'when']
greeting = ['hello', 'hola', 'hi', 'hey']
you = ['yo', 'your', "yo're"]

# Re-set all variables


def reset():
    global usrsentences
    global filtered_sentence
    global response

    usrsentences = []
    filtered_sentence = []
    response = ''

# Get response from user input


def getResponse(command):
    # Obtaining global variables
    global response
    global filtered_sentence

    # Reset filtered sentence
    filtered_sentence = command

    # Generating response
    if filtered_sentence != []:
        if any(question in filtered_sentence for question in question):
            response = "I'm not sure."
        elif any(greeting in filtered_sentence for greeting in greeting):
            response = "Hi."
        else:
            response = "Sorry, I do not understand."

    return response

# Main function for obtaining user input


def main():
    # Obtaining global variables
    global usrsentences
    global response
    global filtered_sentence

    # Getting user input
    usrinput = raw_input('Say: ').lower()
    if usrinput == '':
        response = 'You entered nothing.'

    # Initializing stopwords to use English
    stop_words = set(stopwords.words('english'))

    # Getting number of sentences inputted
    sentences = sent_tokenize(usrinput)
    numsents = len(sentences)

    # Only getting basic meaning if user is not talking to Lukio
    if not any(you in usrinput for you in you):
        # If the input is more than one sentence
        if numsents > 1:
            # Filter each individual sentence and get response
            for i in xrange(numsents):
                # Filtering sentence i
                words = word_tokenize(sentences[i])
                for w in words:
                    if w not in stop_words:
                        filtered_sentence.append(w)

                # Adding filtered sentence to response list if it is not already there
                if len(usrsentences) > 0:
                    if getResponse(filtered_sentence) != unicode(usrsentences[len(usrsentences) - 1]):
                        usrsentences.append(getResponse(filtered_sentence))
                else:
                    usrsentences.append(getResponse(filtered_sentence))

                # Iterating through i
                i += 1

            # Getting final response
            response = unicode(' '.join(usrsentences)).strip()

        # If input is just one sentence
        else:
            words = word_tokenize(usrinput)
            for w in words:
                if w not in stop_words:
                    filtered_sentence.append(w)

            # Get response for filtered sentence
            response = getResponse(filtered_sentence)

    # Making sure it didn't filter out everything
    elif response == '':
        response = getResponse(usrinput)
    else:
        response = getResponse(usrinput)

    # Displaying response
    print filtered_sentence
    print response
    response = ''

    # Re-setting variables
    reset()

    # Loop back
    main()


main()
