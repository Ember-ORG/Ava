from __future__ import absolute_import
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import atime
import asearch
import glob

# Defining variables
num_says = []
response = ''
usrinput = ''

# Word dictionary
you = ['you', 'your', "you're", 'dude']
mean = ['stupid', 'dumb', 'idiot', 'suck', "unintelligent",
        'ignorant', 'brainless', 'idiotic', 'mindless', 'retard']
nice = ['smart', 'intelligent', "clever", "cool", "good", 'nice', 'effecient']
feel = ['feeling', 'feeling', 'feel', 'doing', 'how']
name = ['name']
thanks = ['thanks', 'thank']
time = ['time']
month = ['month']
date = ['date']
year = ['year']
day = ['day', 'today']
clear = ['clear']
understand = ['think', 'know', 'wonder']

# Main AI
def respond(usrinput):
    # Re-set all variables
    def reset():
        global filtered_sentence
        global response

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
            if any(time in filtered_sentence for time in time):
                response = atime.getTime()

            elif any(day in filtered_sentence for day in day):
                response = atime.getDay()

            elif any(month in filtered_sentence for month in month):
                response = atime.getMonth()

            elif any(date in filtered_sentence for date in date):
                response = atime.getDate()

            elif any(year in filtered_sentence for year in year):
                response = atime.getYear()

            elif any(you in filtered_sentence for you in you):
                if any(understand in filtered_sentence for understand in understand):
                    response = "I'm not sure"
                elif any(mean in filtered_sentence for mean in mean):
                    response = "That's not very nice"
                elif any(name in filtered_sentence for name in name):
                    response = "My name is Ava"
                elif any(feel in filtered_sentence for feel in feel):
                    response = 'I am feeling well.'
                elif any(thanks in filtered_sentence for thanks in thanks):
                    response = "You're welcome!"
                elif any(nice in filtered_sentence for nice in nice):
                    response = "Thank you!"
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
        global response
        global filtered_sentence

        # Re-setting variables
        reset()
        
        # Setup usrinput
        usrinput = usrinput.replace("'s", ' is')

        # Initializing stopwords to use English
        stop_words = set(stopwords.words('english'))

        words = word_tokenize(usrinput)
        for w in words:
            if w not in stop_words:
                filtered_sentence.append(w)

        # Get response for filtered sentence
        response = getResponse(filtered_sentence)

        # Making sure it didn't filter out everything
        if response == '':
            response = getResponse(usrinput)

        # Returning response
        return response

    # Call main function
    return main(usrinput)
