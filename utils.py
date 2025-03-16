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
from databaseDataInsert import *
from dataModels import *
from databaseDataSelect import *
from emailSender import *

## USER ##

# LOGIN #

def login(user: UserLogin):
    """
    Attempts to log in a user with the provided credentials.

    Parameters:
        user (UserLogin): An object containing the username and password.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the login attempt.

    Example:
        response = login(UserLogin(username="username123", password="password123"))
    """
    return attemptLogin(user.username, user.password)

# REGISTRATION #

def register(user: RegisterUser):
    """
    Registers a new user after validating the provided information.

    Parameters:
        user (RegisterUser): An object containing the user's registration details.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the registration attempt.

    Example:
        response = register(RegisterUser(username="username123", firstName="Example", lastName="Example", email="example.email@example.com", birthDay=1, birthMonth=1, birthYear=1990, password="password123", gender="M"))
    """
    if not isValidBirthdate(user):
        return PostResponse(statusCode=400, message="REGISTER_FAILED_INVALID_BIRTHDATE")
    elif searchForUserWithEmail(user.email):
        return PostResponse(statusCode=400, message="REGISTER_FAILED_USERNAME_USED")
    elif searchForUserWithUsername(user.username):
        return PostResponse(statusCode=400, message="REGISTER_FAILED_EMAIL_USED")
    addUserToDatabase(user.username, user.firstName, user.lastName, user.email, f"{user.birthDay}/{user.birthMonth}/{user.birthYear}", getEncryptedPassword(user.password), user.gender)
    return PostResponse(statusCode=200, message="REGISTER_OK")

# USER DETAILS #

def getUserData(username): 
    """
    Retrieves the details of a user based on their username.

    Parameters:
        username (str): The username of the user.

    Returns:
        UserData: An object containing the user's details, or False if the user is not found.

    Example:
        user_data = getUserData("example123")
    """
    user = searchForUserDetails(username)
    if user:
        return user
    return False

# GET SESSIONS #

def getUserSessions(username, type):
    """
    Retrieves the sessions joined by a user based on the session type.

    Parameters:
        username (str): The username of the user.
        type (str): The type of sessions to retrieve (e.g., "joinable", "previous").

    Returns:
        list: A list of sessions joined by the user.

    Example:
        sessions = getUserSessions("example123", "joinable")
    """
    return searchForJoinedSessions(username, type) 

def getSessionData(username):
    """
    Retrieves the sessions that a user can sign up for.

    Parameters:
        username (str): The username of the user.

    Returns:
        list: A list of signable sessions.

    Example:
        sessions = getSessionData("example123")
    """
    return searchForSignableSessions(username)

# SIGN IN SESSION #

def saveSignInSession(sessionSignData: SessionSignData):
    """
    Signs a user into a session.

    Parameters:
        sessionSignData (SessionSignData): An object containing the session ID and username.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the sign-in attempt.

    Example:
        response = saveSignInSession(SessionSignData(sessionId=1, username="example123"))
    """
    if addToSessionSigning(sessionSignData.sessionId, sessionSignData.username):
        return PostResponse(statusCode=200, message="SIGN_IN_OK")
    return PostResponse(statusCode=400, message="SIGN_IN_FAIL")

# SIGN OUT SESSION #

def saveSignOutSession(sessionSignData: SessionSignData):
    """
    Signs a user out of a session.

    Parameters:
        sessionSignData (SessionSignData): An object containing the session ID and username.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the sign-out attempt.

    Example:
        response = saveSignOutSession(SessionSignData(sessionId=1, username="example123"))
    """
    if removeFromSessionSigning(sessionSignData.sessionId, sessionSignData.username): 
        return PostResponse(statusCode=200, message="SIGN_OUT_OK")
    return PostResponse(statusCode=400, message="SIGN_OUT_FAIL")

# GET SUMMARY #

def getSessionSummaryData(sessionSignData: SessionSignData):
    """
    Retrieves the summary data for a session.

    Parameters:
        sessionSignData (SessionSignData): An object containing the session ID and username.

    Returns:
        SessionSummary: An object containing the session summary data.

    Example:
        summary = getSessionSummaryData(SessionSignData(sessionId=1, username="example123"))
    """
    return searchForSessionSummary(sessionSignData.username, sessionSignData.sessionId)

def getSession(sessionId: str):
    """
    Retrieves the details of a session based on its ID.

    Parameters:
        sessionId (str): The ID of the session.

    Returns:
        Session: An object containing the session details.

    Example:
        session = getSession("1")
    """
    return searchForSession(sessionId)

# SEND SUMMARY #

def sendSessionSummaryData(sessionId, username, measurements, hrv):
    """
    Saves the summary data for a session.

    Parameters:
        sessionId (str): The ID of the session.
        username (str): The username of the user.
        measurements (list): A list of heart rate measurements.
        hrv (float): The heart rate variability.

    Example:
        sendSessionSummaryData("1", "example123", [70, 80, 90], 50.0)
    """
    addToSessionSummary(sessionId, username, len(measurements), int(average(measurements)), max(measurements), min(measurements), hrv)

def average(arr):
    """
    Calculates the average of a list of numbers.

    Parameters:
        arr (list): A list of numbers.

    Returns:
        float: The average of the numbers.

    Example:
        avg = average([70, 80, 90])
    """
    return sum(arr) / len(arr)

# PASSWORD RECOVERY #

def sendRecoveryEmailToUser(username, code, languageCode):
    """
    Sends a password recovery email to a user.

    Parameters:
        username (str): The username of the user.
        code (str): The recovery code.
        languageCode (str): The language code for the email content.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the email sending attempt.

    Example:
        response = sendRecoveryEmailToUser("example123", "123456", "en")
    """
    user = getUserData(username)
    if user is not None:
        emailResult = sendRecoveryEmail(EMAIL, APP_PASS, user.email, code, languageCode, f'{user.firstName} {user.lastName}')
        if emailResult == 1:
            return PostResponse(statusCode=200, message="EMAIL_SENT")
        return PostResponse(statusCode=400, message="EMAIL_NOT_SENT")

def changeUserPassword(username, newPassword):
    """
    Changes the password of a user.

    Parameters:
        username (str): The username of the user.
        newPassword (str): The new password.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the password change attempt.

    Example:
        response = changeUserPassword("johndoe", "newpassword123")
    """
    if changePassword(username, getEncryptedPassword(newPassword)) != 0:
        return PostResponse(statusCode=200, message="CHANGE_PASS_OK")
    return PostResponse(statusCode=400, message="CHANGE_PASS_FAIL")

## TEACHER ##

# Session Creation 
def createNewSession(sessionCreationData):
    """
    Creates a new session in the database.

    Parameters:
        sessionCreationData (SessionCreationData): An object containing the session details.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the session creation attempt.

    Example:
        response = createNewSession(SessionCreationData(name="Pilates", teacher="Example", description="Simple Pilates", date="2023-10-15", hour="10h", totalSpots=20))
    """
    if addSessionToDatabase(sessionCreationData.name, sessionCreationData.teacher, sessionCreationData.description, sessionCreationData.date, sessionCreationData.hour, sessionCreationData.totalSpots) != 0:
        return PostResponse(statusCode=200, message="CREATE_SESSION_OK")
    return PostResponse(statusCode=400, message="CREATE_SESSION_FAIL")

# Teacher Login
def attemptTeacherLogin(teacherLoginData):
    """
    Attempts to log in a teacher with the provided credentials.

    Parameters:
        teacherLoginData (TeacherLoginData): An object containing the teacher's login details.

    Returns:
        TeacherLoginData: The teacher's login data if successful, or a PostResponse with an error message.

    Example:
        response = attemptTeacherLogin(TeacherLoginData(name="example123", password="password123"))
    """
    if isTeacher(teacherLoginData.name, teacherLoginData.password):
        return teacherLoginData
    return PostResponse(statusCode=400, message="LOGIN_FAIL")

# Session Cancel
def sendCancelEmailToUsers(sessionId):
    """
    Sends a cancellation email to all users signed up for a session.

    Parameters:
        sessionId (str): The ID of the session.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the email sending attempt.

    Example:
        response = sendCancelEmailToUsers("1")
    """
    session = getSession(sessionId)
    usernames = getUsersFromSession(sessionId)
    if session is not None and usernames is not None:
        for username in usernames:
            user = getUserData(username[0])
            if user is not None:
                return sendCancelationEmail(EMAIL, APP_PASS, user.email, f'{user.firstName} {user.lastName}', session)

# Search teacher sessions
def searchTeacherSessions(teacherSessionData):
    """
    Retrieves the sessions associated with a teacher.

    Parameters:
        teacherSessionData (TeacherSessionData): An object containing the teacher's name and session type.

    Returns:
        list: A list of sessions associated with the teacher.

    Example:
        sessions = searchTeacherSessions(TeacherSessionData(name="Example", type="joinable"))
    """
    return searchForTeacherSessions(teacherSessionData.name, teacherSessionData.type)

# Session cancel 
def attemptSessionCancel(sessionCancelData):
    """
    Attempts to cancel a session.

    Parameters:
        sessionCancelData (SessionCancelData): An object containing the session ID and teacher's name.

    Returns:
        bool: True if the session was successfully canceled, False otherwise.

    Example:
        success = attemptSessionCancel(SessionCancelData(name="Example", sessionId="1"))
    """
    if sessionExistsWithTeacher(sessionCancelData.name, sessionCancelData.sessionId):
        sendCancelEmailToUsers(sessionCancelData.sessionId)
        return cancelSession(sessionCancelData.sessionId) != 0
    return False

# Session start
def attemptSessionStart(sessionStartData):
    """
    Attempts to start a session.

    Parameters:
        sessionStartData (SessionStartData): An object containing the session ID.

    Returns:
        bool: True if the session was successfully started, False otherwise.

    Example:
        success = attemptSessionStart(SessionStartData(sessionId="1"))
    """
    if sessionIsToday(sessionStartData.sessionId) and setSessionToActive(sessionStartData.sessionId):
        sendStartEmailToSignedUsers(sessionStartData)
        return True
    return False

def sendStartEmailToSignedUsers(sessionStartData):
    """
    Sends a session start email to all signed-up users.

    Parameters:
        sessionStartData (SessionStartData): An object containing the session ID, Zoom ID, and Zoom password.

    Returns:
        PostResponse: An object containing the status code and message indicating the result of the email sending attempt.

    Example:
        response = sendStartEmailToSignedUsers(SessionStartData(sessionId="1", zoomId="123456", zoomPassword="123456"))
    """
    session = getSession(sessionStartData.sessionId)
    usernames = getUsersFromSession(sessionStartData.sessionId)
    if session is not None and usernames is not None:
        for username in usernames:
            user = getUserData(username[0])
            if user is not None:
                return sendSessionStartEmail(EMAIL, APP_PASS, user.email, f'{user.firstName} {user.lastName}', session, sessionStartData.zoomId, sessionStartData.zoomPassword)

# Session close
def attemptSessionClose(sessionCloseData):
    """
    Attempts to close a session.

    Parameters:
        sessionCloseData (SessionCloseData): An object containing the session ID.

    Returns:
        bool: True if the session was successfully closed, False otherwise.

    Example:
        success = attemptSessionClose(SessionCloseData(sessionId="1"))
    """
    if sessionIsToday(sessionCloseData.sessionId) and setSessionToInactive(sessionCloseData.sessionId):
        return True
    return False

# SSE Session utils
async def getSSEPostResponse(sessionId, username, timestamp, event, value= ""):
    """
    Generates an SSE (Server-Sent Events) response for session updates.

    Parameters:
        sessionId (str): The ID of the session.
        username (str): The username of the user.
        timestamp (str): The timestamp of the event.
        event (str): The type of event.
        value (str, optional): Additional data for the event.

    Returns:
        SSEData: An object containing the SSE data.

    Example:
        sse_data = await getSSEPostResponse("1", "example123", "10000", "session_start")
    """
    return SSEData(sessionId= sessionId, username= username, timeStamp= timestamp, event= event, value= value)

# Token Generation
def generateLoginToken():
    """
    Generates a secure login token.

    Returns:
        str: A hexadecimal token.

    Example:
        token = generateLoginToken()
    """
    return secrets.token_hex(32)

# Password Encryption
def getEncryptedPassword(password):
    """
    Encrypts a password using a salt and PBKDF2-HMAC-SHA256.

    Parameters:
        password (str): The password to encrypt.

    Returns:
        bytes: The encrypted password.

    Example:
        encrypted_password = getEncryptedPassword("password123")
    """
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed_password