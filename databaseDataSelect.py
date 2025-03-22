import sqlite3
from dataModels import *
from databaseOutputParser import *
import logging
import hashlib
import os
from argon2 import PasswordHasher

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
ph = PasswordHasher()

def attemptLogin(username, password):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
        SELECT * 
        FROM user 
        WHERE username = ?
        """
        
        cursor.execute(select_query, (username,))
        user = cursor.fetchone()
        if user and verifyPassword(user[5], password):
            return True
        else:
            return False
    except sqlite3.Error as e:
        logger.error(f"Database error in attemptLogin: {e}")
        return False
    finally:
        if connection:
            connection.close()

def verifyPassword(stored_password: str, password: str):
    """
    Verifies a password against a stored Argon2 hash.

    Parameters:
        stored_password (str): The stored hashed password.
        password (str): The password to verify.

    Returns:
        bool: True if the password matches, False otherwise.

    Example:
        stored_password = getEncryptedPassword("password123")
        is_valid = verifyPassword(storedPassword123, "password123")
    """
    if not password or not stored_password:
        raise ValueError("Password and stored password cannot be empty")
    try:
        return ph.verify(stored_password, password)
    except Exception:
        return False
    
def searchForUserWithEmail(email):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
        SELECT * 
        FROM user 
        WHERE email = ?
        """
        
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForUserWithEmail: {e}")
        return False
    finally:
        if connection:
            connection.close()

def searchForUserWithUsername(username):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
        SELECT * 
        FROM user 
        WHERE username = ?
        """
        
        cursor.execute(select_query, (username,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForUserWithUsername: {e}")
        return False
    finally:
        if connection:
            connection.close()

def searchForSignableSessions(username):
    signableSessions = []
    try:
        for signableId in searchForSignableSessionsIds(username):
            session = searchForSession(signableId[0])
            if session is not None and not isPastDate(session.date):
                signableSessions.append(session)
    except Exception as e:
        logger.error(f"Error in searchForSignableSessions: {e}")
    return signableSessions

def searchForSignableSessionsIds(username):
    connection = None
    try:
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
        return session_ids
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForSignableSessionsIds: {e}")
        return []
    finally:
        if connection:
            connection.close()

def searchForSession(sessionId):
    connection = None
    try:
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
        if session:
            return parseSessionOutput(session, getNumberOfUsersInSession(sessionId), searchForTeacherName(session[2]))
        else:
            return None
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForSession: {e}")
        return None
    finally:
        if connection:
            connection.close()

def searchForTeacherName(username):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
            SELECT name
            FROM teacher
            WHERE username = ?
            """
        
        cursor.execute(select_query, (username,))
        name = cursor.fetchone()
        if name:
            return name[0]
        else:
            return username
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForSession: {e}")
        return username
    finally:
        if connection:
            connection.close()

def getNumberOfUsersInSession(sessionId):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
            SELECT username
            FROM sessionSigning
            WHERE sessionId = ?
            """
        
        cursor.execute(select_query, (sessionId,))
        signings = cursor.fetchall()
        return len(signings)
    except sqlite3.Error as e:
        logger.error(f"Database error in getNumberOfUsersInSession: {e}")
        return 0
    finally:
        if connection:
            connection.close()

def searchForJoinedSessions(username, type):
    joinableSessions = []
    try:
        for signableId in searchForJoinedSessionsIds(username):
            session = searchForSession(signableId[0])
            if session is not None:
                date = session.date
                if (isJoinable(type, date) and (searchForSessionSummary(username, session.id) is None) and session.isActive) or (isPrevious(type, date) and searchForSessionSummary(username, session.id)) or isSignOut(type, date):
                    joinableSessions.append(session)
    except Exception as e:
        logger.error(f"Error in searchForJoinedSessions: {e}")
    return joinableSessions

def searchForJoinedSessionsIds(username):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
            SELECT DISTINCT sessionId
            FROM sessionSigning
            WHERE username = ?
            """
        
        cursor.execute(select_query, (username,))
        session_ids = cursor.fetchall()
        return session_ids
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForJoinedSessionsIds: {e}")
        return []
    finally:
        if connection:
            connection.close()

def searchForSessionSummary(username, sessionId):
    connection = None
    try:
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
        if sessionSummary and session:
            return parseSessionSummaryOutput(session, sessionSummary)
        return None
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForSessionSummary: {e}")
        return None
    finally:
        if connection:
            connection.close()

def searchForUserDetails(username):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
        SELECT * 
        FROM user 
        WHERE username = ?
        """

        cursor.execute(select_query, (username,))
        user = cursor.fetchone()
        if user:
            return parseUserOutput(user)
        return None
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForUserDetails: {e}")
        return None
    finally:
        if connection:
            connection.close()

def isTeacher(name, password):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
        SELECT * 
        FROM teacher 
        WHERE username = ? 
        AND password = ?
        """

        cursor.execute(select_query, (name, password,))
        teacher = cursor.fetchone()
        if teacher:      
            return True
        return False
    except sqlite3.Error as e:
        logger.error(f"Database error in isTeacher: {e}")
        return False
    finally:
        if connection:
            connection.close()

def getUsersFromSession(sessionId):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
        SELECT username 
        FROM sessionSigning 
        WHERE sessionId = ? 
        """

        cursor.execute(select_query, (sessionId,))
        usernames = cursor.fetchall()
        return usernames
    except sqlite3.Error as e:
        logger.error(f"Database error in getUsersFromSession: {e}")
        return []
    finally:
        if connection:
            connection.close()

def searchForTeacherSessions(teacherName, type):
    joinableSessions = []
    try:
        for signableId in searchForJoinedTeacherSessionsIds(teacherName):
            session = searchForSession(signableId[0])
            if session is not None:
                date = session.date
                if (isJoinable(type, date)) or isSignOut(type, date):
                    joinableSessions.append(session)
    except Exception as e:
        logger.error(f"Error in searchForTeacherSessions: {e}")
    return joinableSessions

def searchForJoinedTeacherSessionsIds(teacher):
    connection = None
    try:
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
        return session_ids
    except sqlite3.Error as e:
        logger.error(f"Database error in searchForJoinedTeacherSessionsIds: {e}")
        return []
    finally:
        if connection:
            connection.close()

def sessionExistsWithTeacher(teacherName, sessionId):
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        select_query = """
        SELECT *
        FROM session
        WHERE teacher = ?
        AND sessionId = ?
        """
        
        cursor.execute(select_query, (teacherName, sessionId,))
        session = cursor.fetchall()
        return len(session) > 0
    except sqlite3.Error as e:
        logger.error(f"Database error in sessionExistsWithTeacher: {e}")
        return False
    finally:
        if connection:
            connection.close()

def sessionIsToday(sessionId):
    try:
        session = searchForSession(sessionId)
        return session is not None and isToday(session.date)
    except Exception as e:
        logger.error(f"Error in sessionIsToday: {e}")
        return False

def canEnterSession(sessionId):
    connection = None
    try:
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
        return len(session) > 0
    except sqlite3.Error as e:
        logger.error(f"Database error in canEnterSession: {e}")
        return False
    finally:
        if connection:
            connection.close()

def canLeaveSession(sessionId, username):
    connection = None
    try:
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
        return len(session) > 0  
    except sqlite3.Error as e:
        logger.error(f"Database error in canLeaveSession: {e}")
        return False
    finally:
        if connection:
            connection.close()