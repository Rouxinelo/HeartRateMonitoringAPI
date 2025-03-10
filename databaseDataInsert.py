import sqlite3
from databaseOutputParser import *

def addSessionToDatabase(sessionId, name, teacher, description, date, hour, spots):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO session (sessionID, name, teacher, description, date, hour, spots)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (sessionId, name, teacher, description, date, hour, spots))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in addSessionToDatabase: {e}")
        return False
    finally:
        connection.close()

def addUserToDatabase(username, firstName, lastName, email, dateOfBirth, password, gender):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO user (username, firstName, lastName, email, dateOfBirth, password, gender)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (username, firstName, lastName, email, dateOfBirth, password, gender))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in addUserToDatabase: {e}")
        return False
    finally:
        connection.close()

def addToSessionSigning(sessionId, username):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO sessionSigning (sessionId, username)
        VALUES (?, ?)
        """
        cursor.execute(insert_query, (sessionId, username))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in addToSessionSigning: {e}")
        return False
    finally:
        connection.close()

def addToSessionSummary(sessionId, username, count, average, maximum, minimum, hrv):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO sessionSummary (sessionId, username, count, average, maximum, minimum, hrv)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (sessionId, username, count, average, maximum, minimum, hrv))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in addToSessionSummary: {e}")
        return False
    finally:
        connection.close()

def removeFromSessionSigning(sessionId, username):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        remove_query = """
        DELETE FROM sessionSigning
        WHERE sessionId = ?
        AND username = ?;
        """
        cursor.execute(remove_query, (sessionId, username))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in removeFromSessionSigning: {e}")
        return False
    finally:
        connection.close()

def changePassword(username, newPassword):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        update_query = """
        UPDATE user
        SET password = ?
        WHERE username = ?
        """
        cursor.execute(update_query, (newPassword, username))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in changePassword: {e}")
        return False
    finally:
        connection.close()

def cancelSession(sessionId):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        delete_query = """
        DELETE from session
        WHERE sessionId = ?
        """
        cursor.execute(delete_query, (sessionId,))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in cancelSession: {e}")
        return False
    finally:
        connection.close()

def setSessionToActive(sessionId):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        update_query = """
        UPDATE session
        SET isActive = 1
        WHERE sessionId = ?
        """
        cursor.execute(update_query, (sessionId,))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in setSessionToActive: {e}")
        return False
    finally:
        connection.close()

def setSessionToInactive(sessionId):
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        update_query = """
        UPDATE session
        SET isActive = -1
        WHERE sessionId = ?
        """
        cursor.execute(update_query, (sessionId,))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in setSessionToInactive: {e}")
        return False
    finally:
        connection.close()
