import sqlite3
from databaseOutputParser import *

def addSessionToDatabase(sessionId, name, teacher, description, date, hour, spots):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO session (sessionID, name, teacher, description, date, hour, spots)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.execute(insert_query, (sessionId, name, teacher, description, date, hour, spots))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0

def addUserToDatabase(username, firstName, lastName, email, dateOfBirth, password, gender):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user (username, firstName, lastName, email, dateOfBirth, password, gender)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.execute(insert_query, (username, firstName, lastName, email, dateOfBirth, password, gender))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0

def addToSessionSigning(sessionId, username):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO sessionSigning (sessionId, username)
    VALUES (?, ?)
    """

    cursor.execute(insert_query, (sessionId, username))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0

def addToSessionData(sessionId, username, secondsTimeStamp, heartRate):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO sessionData (sessionId, username, secondsTimeStamp, heartRate)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(insert_query, (sessionId, username, secondsTimeStamp, heartRate))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0

def addToSessionSummary(sessionId, username, count, average, maximum, minimum):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO sessionSummary (sessionId, username, count, average, maximum, minimum)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(insert_query, (sessionId, username, count, average, maximum, minimum))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0

def removeFromSessionSigning(sessionId, username):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    remove_query = """
    DELETE FROM sessionSigning
    WHERE sessionId = ?
    AND username = ?;
    """

    cursor.execute(remove_query, (sessionId, username))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0
        
def addToHeartRateInfo(sessionId, username, heartRate, timeStamp):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO sessionData (sessionId, username, timestamp, heartRate)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(insert_query, (sessionId, username, timeStamp, heartRate))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0    

def changePassword(username, newPassword):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    update_query = """
    UPDATE user
    SET password = ?
    WHERE username = ?
    """

    cursor.execute(update_query, (newPassword, username))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0   

def cancelSession(sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    delete_query = """
    DELETE from session
    WHERE sessionId = ?
    """

    cursor.execute(delete_query, (sessionId,))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0   

def setSessionToActive(sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    update_query = """
    UPDATE session
    SET isActive = 1
    WHERE sessionId = ?
    """

    cursor.execute(update_query, (sessionId,))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0  

def setSessionToInactive(sessionId):
    connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
    cursor = connection.cursor()
    update_query = """
    UPDATE session
    SET isActive = -1
    WHERE sessionId = ?
    """

    cursor.execute(update_query, (sessionId,))
    connection.commit()
    connection.close()
    return cursor.rowcount != 0    