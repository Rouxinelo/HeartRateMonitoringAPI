from dataModels import *
from datetime import datetime

def parseUserOutput(user): 
    return UserData(username=user[0], 
             email= user[3], 
             firstName= user[1], 
             lastName= user[2], 
             age= getUserAgeFromDate(user[4]), 
             gender=user[6])
    
def getUserAgeFromDate(date):
    dateFormat = "%d/%m/%Y"
    birthDate = datetime.strptime(date, dateFormat)
    today = datetime.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age

def parseSessionOutput(session, filledSpots, teacherName):
    return Session(id= str(session[0]), 
                   name= session[1], 
                   date= session[4], 
                   hour= str(session[5]), 
                   teacher= teacherName, 
                   totalSpots= session[6], 
                   filledSpots= filledSpots, 
                   description= session[3], 
                   isActive= session[7])

def parseSessionSummaryOutput(session, sessionSummary):
    return PreviousSessionData(session=session, 
                               count=sessionSummary[2], 
                               average= sessionSummary[3], 
                               maximum= sessionSummary[4], 
                               minimum= sessionSummary[5],
                               hrv= sessionSummary[6])

# Used to get a date string
def getCurrentTimeStamp():
    return datetime.now().isoformat(timespec="seconds")

def isJoinable(type, date):
    return type == "joinable" and userCanJoin(date)

def isPrevious(type, date):
    return type == "previous" and userCanSeeSummary(date)

def isSignOut(type, date):
    return type == "signed" and userSignOut(date)

def userCanJoin(dateStr):
    date = datetime.strptime(dateStr, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() == today

def userCanSeeSummary(date_str):
    date = datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() <= today

def userSignOut(date_str):
    date = datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() > today

def isPastDate(date_str):
    date = datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() < today

def isToday(date_str):
    date = datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() == today