from dataModels import *
from commons import *

def parseUserOutput(user): 
    """
    Parses raw user data into a `UserData` object.

    Parameters:
        user (list or tuple): A list or tuple containing user data in the following order:
            - username (str): The username of the user.
            - firstName (str): The first name of the user.
            - lastName (str): The last name of the user.
            - email (str): The email address of the user.
            - dateOfBirth (str): The date of birth of the user in the format "dd/mm/yyyy".
            - gender (str): The gender of the user.

    Returns:
        UserData: An object containing the parsed user data.

    Example:
        user_data = parseUserOutput(("example123", "Example", "Name", "example.email@example.com", "01/01/1990", "M"))
    """
    return UserData(
        username=user[0],
        email=user[3],
        firstName=user[1],
        lastName=user[2],
        age=getUserAgeFromDate(user[4]),
        gender=user[6]
    )

def parseSessionOutput(session, filledSpots, teacherName):
    """
    Parses raw session data into a `Session` object.

    Parameters:
        session (list or tuple): A list or tuple containing session data in the following order:
            - id (int): The ID of the session.
            - name (str): The name of the session.
            - date (str): The date of the session.
            - hour (str): The hour of the session.
            - totalSpots (int): The total number of spots available in the session.
            - description (str): A description of the session.
            - isActive (int): A flag indicating whether the session is active (1) or inactive (-1).
        filledSpots (int): The number of spots already filled in the session.
        teacherName (str): The name of the teacher conducting the session.

    Returns:
        Session: An object containing the parsed session data.

    Example:
        session_data = parseSessionOutput((1, "Pilates", "2023-10-15", "10", 20, "Simple Pilates", 1), 15, "Example123")
    """
    return Session(
        id=str(session[0]),
        name=session[1],
        date=session[4],
        hour=str(session[5]),
        teacher=teacherName,
        totalSpots=session[6],
        filledSpots=filledSpots,
        description=session[3],
        isActive=session[7]
    )

def parseSessionSummaryOutput(session, sessionSummary):
    """
    Parses raw session summary data into a `PreviousSessionData` object.

    Parameters:
        session (Session): A `Session` object representing the session.
        sessionSummary (list or tuple): A list or tuple containing session summary data in the following order:
            - count (int): The count of heart rate measurements.
            - average (int): The average heart rate.
            - maximum (int): The maximum heart rate.
            - minimum (int): The minimum heart rate.
            - hrv (int): The heart rate variability.

    Returns:
        PreviousSessionData: An object containing the parsed session summary data.

    Example:
        summary_data = parseSessionSummaryOutput(session, (100, 75, 120, 60, 50))
    """
    return PreviousSessionData(
        session=session,
        count=sessionSummary[2],
        average=sessionSummary[3],
        maximum=sessionSummary[4],
        minimum=sessionSummary[5],
        hrv=sessionSummary[6]
    )