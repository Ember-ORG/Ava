from __future__ import absolute_import
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import atime
import asearch
import glob


# Defining variables
num_says = []
multsent = False
usrsentences = []
response = ''
numsents = 0
sentcount = 0
usrinput = ''
understand = False

# Word dictionary
question = ['what', 'where', 'why', 'how', 'when', 'do', 'does']
greeting = ['hello', 'hola', 'hi', 'hey']
you = ['yo', 'your', "yo're", 'dude', 'my dude', 'my guy']
whats = ["what's", 'whats']
up = ['poppin', "poppin'", "up"]
favorite = ['favorite']
color = ['color']
mean = ['stupid', 'dumb', 'idiot', 'suck', "unintelligent",
        'ignorant', 'brainless', 'idiotic', 'mindless', 'dumbass', 'retard']
nice = ['smart', 'intelligent', "clever", "cool", "good", 'nice']
basic = ['ok', 'good', 'sounds fine',
         'alright', 'fine', 'yes', 'no', 'yeah']
food = ['food', 'foods']
feel = ['feeling', 'feeling', 'feel', 'doing', 'how']
name = ['name']
thanks = ['thanks', 'thank']
book = ['book']
time = ['time']
month = ['month']
date = ['date']
year = ['year']
day = ['day', 'today']
creators = ['creators', 'created', 'made', 'are', 'who']
clear = ['clear']
understand = ['think', 'know', 'wonder']

# Main AI
def respond(usrinput):
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
            if any(greeting in filtered_sentence for greeting in greeting):
                response = "Hi."

            elif any(basic in filtered_sentence for basic in basic):
                response = "Ok."

            elif any(time in filtered_sentence for time in time):
                response = atime.getTime()

            elif any(day in filtered_sentence for day in day):
                response = atime.getDay()

            elif any(month in filtered_sentence for month in month):
                response = atime.getMonth()

            elif any(date in filtered_sentence for date in date):
                response = atime.getDate()

            elif any(year in filtered_sentence for year in year):
                response = atime.getYear()

            elif any(clear in filtered_sentence for clear in clear):
                response = "Clearing cached speech files"
                files = glob.glob('/tts/*')
                for f in files:
                    os.remove(f)

            elif any(whats in filtered_sentence for whats in whats) and any(up in filtered_sentence for up in up):
                response = "Not much my guy"

            elif any(you in filtered_sentence for you in you):
                if any(understand in filtered_sentence for understand in understand):
                    response = "I'm not sure"
                if any(mean in filtered_sentence for mean in mean):
                    response = "That's not very nice"
                elif any(name in filtered_sentence for name in name):
                    response = "My name is Ava"
                elif any(feel in filtered_sentence for feel in feel):
                    response = 'I am feeling well.'
                elif any(creators in filtered_sentence for creators in creators):
                    response = "I am an open source assistant made by Ian Draves, Oscar Rhoades, and Davis Dova loce Dell osh."
                elif any(thanks in filtered_sentence for thanks in thanks):
                    response = "Yo're welcome!"
                elif any(nice in filtered_sentence for nice in nice):
                    response = "Thank you!"
                elif any(food in filtered_sentence for food in food):
                    response = "I dont't eat food, I am a robot"
                elif any(color in filtered_sentence for color in color):
                    response = "I love colors, my favorite color is blue"
                elif any(favorite in filtered_sentence for favorite in favorite):
                    if any(food in filtered_sentence for food in food):
                        response = "I am a robot, I do not have a favorite food."
                    elif any(book in filtered_sentence for book in book):
                        response = "I don't read books"
                    elif any(color in filtered_sentence for color in color):
                        response = 'My favorite color is blue.'
                elif response == "":
                    response = "Sorry I do not understand"
                else:
                    response = "Sorry I do not understand"

            else:
                response = asearch.ddg(' '.join(filtered_sentence)).strip()
                if response == 'null_result' or response == '':
                    response = asearch.wiki(
                        ' '.join(filtered_sentence)).strip()
                    if response == 'null_result':
                        response = "Sorry, I do not understand."

        return response

    # Main function for obtaining user input
    def main(usrinput):
        # Obtaining global variables
        global usrsentences
        global response
        global filtered_sentence

        # Re-setting variables
        reset()

        # Initializing stopwords to use English
        stop_words = set(stopwords.words('english'))

        # Getting number of sentences inputted
        sentences = sent_tokenize(usrinput)
        numsents = len(sentences)

        # Only getting basic meaning if user is not talking to Ava
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

        # Returning response
        return response

    # Call main function
    return main(usrinput)
