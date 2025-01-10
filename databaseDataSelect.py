import sqlite3
from dataModels import *
from databaseOutputParser import *
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

# Login - Its simplified and would be better to develop a more complex version in the future 
def attemptLogin(username, password):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT * 
    FROM user 
    WHERE username = ? 
    AND password = ?
    """
    
    cursor.execute(select_query, (username, password))
    user = cursor.fetchone()
    connection.close()
    if user:
        return True
    else:
        return False
    
# Searching for user for login actions (see is the username or email are already registered before moving on)
def searchForUserWithEmail(email):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT * 
    FROM user 
    WHERE email = ?
    """
    
    cursor.execute(select_query, (email,))
    user = cursor.fetchone()
    connection.close()
    if user:
        return True
    else:
        return False

def searchForUserWithUsername(username):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT * 
    FROM user 
    WHERE username = ?
    """
    
    cursor.execute(select_query, (username,))
    user = cursor.fetchone()
    connection.close()
    if user:
        return True
    else:
        return False
 
# Searching for joinable sessions logic 

def searchForSignableSessions(username):
    signableSessions = []
    for signableId in searchForSignableSessionsIds(username):
        session = searchForSession(signableId[0])
        if session is not None and not isPastDate(session.date):
            signableSessions.append(session)
    return signableSessions

def searchForSignableSessionsIds(username):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
        SELECT DISTINCT sessionId
        FROM session
        EXCEPT
        SELECT sessionId
        FROM sessionSigning
        WHERE username = ?
        """
    
    cursor.execute(select_query, (username,))
    session_ids = cursor.fetchall()
    connection.close()
    return session_ids

def searchForSession(sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
        SELECT *
        FROM session
        WHERE sessionId = ?
        AND isActive != -1
        """
    
    cursor.execute(select_query, (sessionId,))
    session = cursor.fetchone()
    connection.close()

    if session:
        return parseSessionOutput(session, getNumberOfUsersInSession(sessionId))
    else:
        return None

def getNumberOfUsersInSession(sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
        SELECT username
        FROM sessionSigning
        WHERE sessionId = ?
        """
    
    cursor.execute(select_query, (sessionId,))
    signings = cursor.fetchall()
    connection.close()

    return len(signings)

# Logic to get user sessions
# 1 - Joinable (Date must be TODAY)

def searchForJoinedSessions(username, type):
    joinableSessions = []
    for signableId in searchForJoinedSessionsIds(username):
        session = searchForSession(signableId[0])
        if session is not None:
            date = session.date
            if (isJoinable(type, date) and (searchForSessionSummary(username, session.id) is None) and session.isActive) or (isPrevious(type, date) and searchForSessionSummary(username, session.id)) or isSignOut(type, date):
                joinableSessions.append(session)
    return joinableSessions

def searchForJoinedSessionsIds(username):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
        SELECT DISTINCT sessionId
        FROM sessionSigning
        WHERE username = ?
        """
    
    cursor.execute(select_query, (username,))
    session_ids = cursor.fetchall()
    connection.close()
    return session_ids


# Logic to get the session summary

def searchForSessionSummary(username, sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT * 
    FROM sessionSummary 
    WHERE username = ? 
    AND sessionId = ?
    """
    
    cursor.execute(select_query, (username, sessionId,))
    sessionSummary = cursor.fetchone()
    session = searchForSession(sessionId)
    connection.close()
    if sessionSummary and session:
        return parseSessionSummaryOutput(session, sessionSummary)
    return None

# Logic to get the user details 

def searchForUserDetails(username):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT * 
    FROM user 
    WHERE username = ?
    """

    cursor.execute(select_query, (username,))
    user = cursor.fetchone()
    connection.close()
    if user:
        return parseUserOutput(user)
    return None

# Logic to get next session id

def getNextSessionId():
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT sessionId
    FROM session 
    ORDER BY sessionId DESC
    LIMIT 1
    """

    cursor.execute(select_query)
    sessionId = cursor.fetchone()
    connection.close()
    if sessionId:      
        return sessionId[0] + 1
    return 1

# Logic to get Login the teacher

def isTeacher(name, password):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT * 
    FROM teacher 
    WHERE name = ? 
    AND password = ?
    """

    cursor.execute(select_query, (name, password,))
    teacher = cursor.fetchone()
    connection.close()
    if teacher:      
        return True
    return False

# Logic to get all users in the session

def getUsersFromSession(sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT username 
    FROM sessionSigning 
    WHERE sessionId = ? 
    """

    cursor.execute(select_query, (sessionId,))
    usernames = cursor.fetchall()
    connection.close()
    return usernames

# Logic to get a teacher sessions

def searchForTeacherSessions(teacherName, type):
    joinableSessions = []
    for signableId in searchForJoinedTeacherSessionsIds(teacherName):
        session = searchForSession(signableId[0])
        if session is not None:
            date = session.date
            if (isJoinable(type, date)) or isSignOut(type, date):
                joinableSessions.append(session)
    return joinableSessions

def searchForJoinedTeacherSessionsIds(teacher):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
        SELECT DISTINCT sessionId
        FROM session
        WHERE teacher = ?
        AND isActive = 0
        """
    
    cursor.execute(select_query, (teacher,))
    session_ids = cursor.fetchall()
    connection.close()
    return session_ids

def sessionExistsWithTeacher(teacherName, sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT *
    FROM session
    WHERE teacher = ?
    AND sessionId = ?
    """
    
    cursor.execute(select_query, (teacher, sessionId,))
    session = cursor.fetchall()
    connection.close()
    return len(session) > 0

# Check if session exists

def sessionIsToday(sessionId):
    session = searchForSession(sessionId)
    return session is not None and isToday(session.date)

# Logic to see if can enter and leave session

def canEnterSession(sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT *
    FROM session
    WHERE sessionId = ?
    AND isActive = 1
    """
    
    cursor.execute(select_query, (sessionId,))
    session = cursor.fetchall()
    connection.close()
    return len(session) > 0

def canLeaveSession(sessionId, username):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    select_query = """
    SELECT *
    FROM sessionSigning
    WHERE sessionId = ?
    AND username = ?
    """
    
    cursor.execute(select_query, (sessionId, username,))
    session = cursor.fetchall()
    connection.close()
    return len(session) > 0  