from dataModels import *
from datetime import datetime

def getCurrentTimeStamp():
    """
    Generates a timestamp for the current date and time.

    Returns:
        str: A string representing the current date and time in ISO format (e.g., "2020-20-20T20:20:00").

    Example:
        timestamp = getCurrentTimeStamp()
    """
    return datetime.now().isoformat(timespec="seconds")

def isJoinable(type, date):
    """
    Checks if a session is joinable based on its type and date.

    Parameters:
        type (str): The type of the session (e.g., "joinable").
        date (str): The date of the session in the format "dd-mm-yyyy".

    Returns:
        bool: True if the session is joinable, False otherwise.

    Example:
        joinable = isJoinable("joinable", "15-10-2023")
    """
    return type == "joinable" and userCanJoin(date)

def isPrevious(type, date):
    """
    Checks if a session is a previous session based on its type and date.

    Parameters:
        type (str): The type of the session (e.g., "previous").
        date (str): The date of the session in the format "dd-mm-yyyy".

    Returns:
        bool: True if the session is a previous session, False otherwise.

    Example:
        previous = isPrevious("previous", "15-10-2023")
    """
    return type == "previous" and userCanSeeSummary(date)

def isSignOut(type, date):
    """
    Checks if a session allows sign-out based on its type and date.

    Parameters:
        type (str): The type of the session (e.g., "signed").
        date (str): The date of the session in the format "dd-mm-yyyy".

    Returns:
        bool: True if the session allows sign-out, False otherwise.

    Example:
        sign_out = isSignOut("signed", "15-10-2023")
    """
    return type == "signed" and userSignOut(date)

def userCanJoin(dateStr):
    """
    Checks if a user can join a session based on the session date.

    Parameters:
        dateStr (str): The date of the session in the format "dd-mm-yyyy".

    Returns:
        bool: True if the session date is today, False otherwise.

    Example:
        can_join = userCanJoin("15-10-2023")
    """
    date = datetime.strptime(dateStr, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() == today

def userCanSeeSummary(date_str):
    """
    Checks if a user can see the summary of a session based on the session date.

    Parameters:
        date_str (str): The date of the session in the format "dd-mm-yyyy".

    Returns:
        bool: True if the session date is today or in the past, False otherwise.

    Example:
        can_see_summary = userCanSeeSummary("15-10-2023")
    """
    date = datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() <= today

def userSignOut(date_str):
    """
    Checks if a user can sign out of a session based on the session date.

    Parameters:
        date_str (str): The date of the session in the format "dd-mm-yyyy".

    Returns:
        bool: True if the session date is in the future, False otherwise.

    Example:
        can_sign_out = userSignOut("15-10-2023")
    """
    date = datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() > today

def isPastDate(date_str):
    """
    Checks if a date is in the past.

    Parameters:
        date_str (str): The date to check in the format "dd-mm-yyyy".

    Returns:
        bool: True if the date is in the past, False otherwise.

    Example:
        past = isPastDate("15-10-2023")
    """
    date = datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() < today

def isToday(date_str):
    """
    Checks if a date is today.

    Parameters:
        date_str (str): The date to check in the format "dd-mm-yyyy".

    Returns:
        bool: True if the date is today, False otherwise.

    Example:
        today = isToday("15-10-2023")
    """
    date = datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.today().date()
    return date.date() == today

def getUserAgeFromDate(date):
    """
    Calculates the age of a user based on their date of birth.

    Parameters:
        date (str): The date of birth in the format "dd/mm/yyyy".

    Returns:
        int: The calculated age.

    Example:
        age = getUserAgeFromDate("01/01/1990")
    """
    dateFormat = "%d/%m/%Y"
    birthDate = datetime.strptime(date, dateFormat)
    today = datetime.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age

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

def isValidBirthdate(user):
    """
    Validates if the provided birthdate is valid and in the past.

    Parameters:
        user (RegisterUser): An object containing the user's birthdate details.

    Returns:
        bool: True if the birthdate is valid and in the past, False otherwise.

    Example:
        valid = isValidBirthdate(RegisterUser(birthDay=1, birthMonth=1, birthYear=1990))
    """
    try:
        birth_date = datetime(user.birthYear, user.birthMonth, user.birthDay)
        return birth_date < datetime.now()
    except ValueError:
        return False