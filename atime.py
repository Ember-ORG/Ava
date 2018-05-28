from __future__ import absolute_import
import datetime
import time
import re


class amTime(object):
    hours = 1
    minutes = 0
    amPm = "AM"
    # Example: 6:30A.M.

    def convertString(self, input):
        input = input.lower()
        colonLocation = input.find(':')
        amPmLoc = colonLocation + 3
        if input[amPmLoc] == 'a':
            self.amPm = "AM"
        if colonLocation == 1:
            self.hours = int(input[0])
        elif colonLocation == 2:
            self.hours = int(input[0:2])
        self.minutes = int(input[(colonLocation+1):(colonLocation+3)])
        input.split()

    def __init__(self, hours, amPm):
        self.hours = hours
        self.amPM = amPm

    def convert(self, hours):
        if dt.hour > 12:
            self.hours = dt.hour - 12
            self.amPm = "PM"
        else:
            self.hours = dt.hour
            self.amPm = "AM"

    def update(self):
        dt = datetime.datetime.today()
        self.convert(dt.hour)
        self.minutes = dt.minute


# Defining time variables
dt = datetime.datetime.today()
alarmTime = amTime(1, "AM")
currentTime = amTime(dt.hour, "PM")
currentTime.update()


def getTime():
    return unicode(unicode(currentTime.hours) + ':' + unicode(currentTime.minutes) + ' ' + currentTime.amPm)


def getDay():
    today = dt.day % 10
    if today == 1:
        response = unicode('Today is the ' + unicode(dt.day) + 'st')
    elif today == 2:
        response = unicode('Today is the ' + unicode(dt.day) + 'nd')
    elif today == 3:
        response = unicode('Today is the ' + unicode(dt.day) + 'rd')
    else:
        response = unicode('Today is the ' + unicode(dt.day) + 'th')

    return response


def getMonth():
    curmonth = dt.month
    if curmonth == 1:
        response = 'January'
    elif curmonth == 2:
        response = 'February'
    elif curmonth == 3:
        response = 'March'
    elif curmonth == 4:
        response = 'April'
    elif curmonth == 5:
        response = 'May'
    elif curmonth == 6:
        response = 'June'
    elif curmonth == 7:
        response = 'July'
    elif curmonth == 8:
        response = 'August'
    elif curmonth == 9:
        response = 'September'
    elif curmonth == 10:
        response = 'October'
    elif curmonth == 11:
        response = 'November'
    else:
        response = 'December'

    return response


def getYear():
    return unicode('The current year is ' + unicode(dt.year))


def getDate():
    return unicode(getMonth + getDay)
