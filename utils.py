# Library Imports
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import logging
from pydantic import BaseModel
import json
import random
import secrets
from threading import Lock
import hashlib
import os

# Created File Imports
from databaseDataInsert import *
from dataModels import *
from databaseDataSelect import *
from emailSender import *

## USER ##

# LOGIN #
 
def login(user: UserLogin):
    return attemptLogin(user.username, user.password)

# REGISTRATION #

def register(user: RegisterUser):
    if not isValidBirthdate(user):
        return PostResponse(statusCode=400, message="REGISTER_FAILED_INVALID_BIRTHDATE")
    elif searchForUserWithEmail(user.email):
        return PostResponse(statusCode=400, message="REGISTER_FAILED_USERNAME_USED")
    elif searchForUserWithUsername(user.username):
        return PostResponse(statusCode=400, message="REGISTER_FAILED_EMAIL_USED")
    addUserToDatabase(user.username, user.firstName, user.lastName, user.email, f"{user.birthDay}/{user.birthMonth}/{user.birthYear}", getEncryptedPassword(user.password), user.gender)
    return PostResponse(statusCode=200, message="REGISTER_OK")

def isValidBirthdate(user):
    try:
        birth_date = datetime(user.birthYear, user.birthMonth, user.birthDay)
        return birth_date < datetime.now()
    except ValueError:
        return False

# USER DETAILS #

def getUserData(username): 
    user = searchForUserDetails(username)
    if user:
        return user
    return False

# GET SESSIONS #

def getUserSessions(username, type):
    return searchForJoinedSessions(username, type) 

def getSessionData(username):
    return searchForSignableSessions(username)

# SIGN IN SESSION #

def saveSignInSession(sessionSignData: SessionSignData):
    if addToSessionSigning(sessionSignData.sessionId, sessionSignData.username):
        return PostResponse(statusCode=200, message="SIGN_IN_OK")
    return PostResponse(statusCode=400, message="SIGN_IN_FAIL")

# SIGN OUT SESSION #

def saveSignOutSession(sessionSignData: SessionSignData):
    if removeFromSessionSigning(sessionSignData.sessionId, sessionSignData.username): 
        return PostResponse(statusCode=200, message="SIGN_OUT_OK")
    return PostResponse(statusCode=400, message="SIGN_OUT_FAIL")

# GET SUMMARY #

def getSessionSummaryData(sessionSignData: SessionSignData):
    return searchForSessionSummary(sessionSignData.username, sessionSignData.sessionId)

def getSession(sessionId: str):
    return searchForSession(sessionId)

# SEND SUMMARY #

def sendSessionSummaryData(sessionId, username, measurements, hrv):
    addToSessionSummary(sessionId, username, len(measurements), int(average(measurements)), max(measurements), min(measurements), hrv)

def average(arr):
    return sum(arr) / len(arr)

# PASSWORD RECOVERY #

def sendRecoveryEmailToUser(username, code, languageCode):
    user = getUserData(username)
    if user is not None:
        emailResult = sendRecoveryEmail(EMAIL, APP_PASS, user.email, code, languageCode, f'{user.firstName} {user.lastName}')
        if emailResult == 1:
            return PostResponse(statusCode=200, message="EMAIL_SENT")
        return PostResponse(statusCode=400, message="EMAIL_NOT_SENT")

def changeUserPassword(username, newPassword):
    if changePassword(username, getEncryptedPassword(newPassword)) != 0:
        return PostResponse(statusCode=200, message="CHANGE_PASS_OK")
    return PostResponse(statusCode=400, message="CHANGE_PASS_FAIL")

## TEACHER ##

# Session Creation 
def createNewSession(sessionCreationData):
    sessionId = getNextSessionId()
    if addSessionToDatabase(sessionId, sessionCreationData.name, sessionCreationData.teacher, sessionCreationData.description, sessionCreationData.date, sessionCreationData.hour, sessionCreationData.totalSpots) != 0:
        return PostResponse(statusCode=200, message="CREATE_SESSION_OK")
    return PostResponse(statusCode=400, message="CREATE_SESSION_FAIL")

# Teacher Login
def attemptTeacherLogin(teacherLoginData):
    if isTeacher(teacherLoginData.name, teacherLoginData.password):
        return teacherLoginData
    return PostResponse(statusCode=400, message="LOGIN_FAIL")


# Session Cancel
def sendCancelEmailToUsers(sessionId):
    session = getSession(sessionId)
    usernames = getUsersFromSession(sessionId)
    if session is not None and usernames is not None:
        for username in usernames:
            user = getUserData(username[0])
            if user is not None:
                return sendCancelationEmail(EMAIL, APP_PASS, user.email, f'{user.firstName} {user.lastName}', session)
        
# Search teacher sessions
def searchTeacherSessions(teacherSessionData):
    return searchForTeacherSessions(teacherSessionData.name, teacherSessionData.type)

# Session cancel 
def attemptSessionCancel(sessionCancelData):
    if sessionExistsWithTeacher(sessionCancelData.name, sessionCancelData.sessionId):
        sendCancelEmailToUsers(sessionCancelData.sessionId)
        return cancelSession(sessionCancelData.sessionId) != 0
    return False

# Session start
def attemptSessionStart(sessionStartData):
    if sessionIsToday(sessionStartData.sessionId) and setSessionToActive(sessionStartData.sessionId):
        sendStartEmailToSignedUsers(sessionStartData)
        return True
    return False

def sendStartEmailToSignedUsers(sessionStartData):
    session = getSession(sessionStartData.sessionId)
    usernames = getUsersFromSession(sessionStartData.sessionId)
    if session is not None and usernames is not None:
        for username in usernames:
            user = getUserData(username[0])
            if user is not None:
                return sendSessionStartEmail(EMAIL, APP_PASS, user.email, f'{user.firstName} {user.lastName}', session, sessionStartData.zoomId, sessionStartData.zoomPassword)


# Session close
def attemptSessionClose(sessionCloseData):
    if sessionIsToday(sessionCloseData.sessionId) and setSessionToInactive(sessionCloseData.sessionId):
        return True
    return False

# SSE Session utils
async def getSSEPostResponse(sessionId, username, timestamp, event, value= ""):
    return SSEData(sessionId= sessionId, username= username, timeStamp= timestamp, event= event, value= value)


# Token Generation
def generateLoginToken():
    return secrets.token_hex(32)

# Password Encryption

def getEncryptedPassword(password):
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed_password