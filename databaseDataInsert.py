import sqlite3
from databaseOutputParser import *

def addSessionToDatabase(name, teacher, description, date, hour, spots):
    """
    Adds a new session to the `session` table in the database.

    Parameters:
        name (str): The name of the session.
        teacher (str): The teacher conducting the session.
        description (str): A description of the session.
        date (str): The date of the session.
        hour (str): The hour of the session.
        spots (int): The number of available spots in the session.

    Returns:
        bool: True if the session was successfully added, False otherwise.

    Example:
        addSessionToDatabase("Pilates", "Example name", "Simple Pilates lesson", "2023-10-15", "10", 20)
    """
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO session (name, teacher, description, date, hour, spots)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (name, teacher, description, date, hour, spots))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in addSessionToDatabase: {e}")
        return False
    finally:
        if connection:
            connection.close()


def addUserToDatabase(username, firstName, lastName, email, dateOfBirth, password, gender):
    """
    Adds a new user to the `user` table in the database.

    Parameters:
        username (str): The username of the user.
        firstName (str): The first name of the user.
        lastName (str): The last name of the user.
        email (str): The email address of the user.
        dateOfBirth (str): The date of birth of the user.
        password (str): The password of the user.
        gender (str): The gender of the user.

    Returns:
        bool: True if the user was successfully added, False otherwise.

    Example:
        addUserToDatabase("exampleUsername", "Example", "Name", "example.email@example.com", "1990-01-01", "password123", "M")
    """
    connection = None
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
        if connection:
            connection.close()


def addToSessionSigning(sessionId, username):
    """
    Adds a user to the `sessionSigning` table, indicating that the user has signed up for a session.

    Parameters:
        sessionId (int): The ID of the session.
        username (str): The username of the user signing up for the session.

    Returns:
        bool: True if the signing was successfully added, False otherwise.

    Example:
        addToSessionSigning(1, "example123")
    """
    connection = None
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
        if connection:
            connection.close()


def addToSessionSummary(sessionId, username, count, average, maximum, minimum, hrv):
    """
    Adds a summary of a session to the `sessionSummary` table, including heart rate statistics.

    Parameters:
        sessionId (int): The ID of the session.
        username (str): The username of the user.
        count (int): The count of heart rate measurements.
        average (int): The average heart rate.
        maximum (int): The maximum heart rate.
        minimum (int): The minimum heart rate.
        hrv (int): The heart rate variability.

    Returns:
        bool: True if the summary was successfully added, False otherwise.

    Example:
        addToSessionSummary(1, "example123", 100, 75, 120, 60, 50)
    """
    connection = None
    try:
        connection = sqlite3.connect("HeartRateMonitoring.sqlite3")
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO sessionSummary (sessionId, username, hrCount, hrAverage, hrMaximum, hrMinimum, hrv)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (sessionId, username, count, average, maximum, minimum, hrv))
        connection.commit()
        return cursor.rowcount != 0
    except Exception as e:
        print(f"Error in addToSessionSummary: {e}")
        return False
    finally:
        if connection:
            connection.close()


def removeFromSessionSigning(sessionId, username):
    """
    Removes a user from the `sessionSigning` table, indicating that the user has canceled their sign-up for a session.

    Parameters:
        sessionId (int): The ID of the session.
        username (str): The username of the user.

    Returns:
        bool: True if the signing was successfully removed, False otherwise.

    Example:
        removeFromSessionSigning(1, "example123")
    """
    connection = None
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
        if connection:
            connection.close()


def changePassword(username, newPassword):
    """
    Updates the password of a user in the `user` table.

    Parameters:
        username (str): The username of the user.
        newPassword (str): The new password.

    Returns:
        bool: True if the password was successfully updated, False otherwise.

    Example:
        changePassword("example123", "newpassword123")
    """
    connection = None
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
        if connection:
            connection.close()


def cancelSession(sessionId):
    """
    Deletes a session from the `session` table.

    Parameters:
        sessionId (int): The ID of the session to be canceled.

    Returns:
        bool: True if the session was successfully canceled, False otherwise.

    Example:
        cancelSession(1)
    """
    connection = None
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
        if connection:
            connection.close()


def setSessionToActive(sessionId):
    """
    Sets a session to active by updating the `isActive` field in the `session` table.

    Parameters:
        sessionId (int): The ID of the session.

    Returns:
        bool: True if the session was successfully set to active, False otherwise.

    Example:
        setSessionToActive(1)
    """
    connection = None
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
        if connection:
            connection.close()


def setSessionToInactive(sessionId):
    """
    Sets a session to inactive by updating the `isActive` field in the `session` table.

    Parameters:
        sessionId (int): The ID of the session.

    Returns:
        bool: True if the session was successfully set to inactive, False otherwise.

    Example:
        setSessionToInactive(1)
    """
    connection = None
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
        if connection:
            connection.close()