from utils import *
from fastapi import Header

app = FastAPI()
event_queue = asyncio.Queue()

sessionTokens = {}
lock = Lock()

# Check if device token if valid 

def isTokenValid(username: str, device_token: str):
    with lock:
        return sessionTokens.get(username) == device_token

@app.get(
    "/",
    summary="Main Path",
    description="""
    Default path for the API. This path is unavailable for use and returns an invalid path message.
    
    Returns:
    - A JSON object with a message indicating the path is invalid.
    """
)
def index():
    return {"path": "Invalid Path"}

@app.post(
    "/login-user",
    summary="User Login",
    description="""
    Authenticates the user and generates a session token if credentials are valid.
    
    Request Body:
    - `username` (string): The user's username.
    - `password` (string): The user's password.

    Responses:
    - If credentials are correct:
      - Returns a `200 OK` status with a session token.
    - If the user is already logged in:
      - Returns a `400 Bad Request` status with the message `ALREADY_LOGGED`.
    - If credentials are incorrect:
      - Returns a `400 Bad Request` status with the message `LOGIN_FAIL`.

    Example Request:
    {
      "username": "username123",
      "password": "password123"
    }
    

    Example Response:
    {
      "statusCode": 200,
      "message": "LOGIN_OK",
      "deviceToken": "abc123xyz"
    }
    """
)
def loginUser(user: UserLogin):
    if login(user):
        with lock:
            if user.username in sessionTokens:
                return LoginResponse(statusCode=400, message="ALREADY_LOGGED", deviceToken="") 
            token = generateLoginToken()
            logger.debug(f"Device-Token: {token}")
            sessionTokens[user.username] = token
        return LoginResponse(statusCode=200, message="LOGIN_OK", deviceToken=token)
    return LoginResponse(statusCode=400, message="LOGIN_FAIL", deviceToken="")

@app.post(
    "/logout-user",
    summary="User Logout",
    description="""
    Logs out the user by removing their session token.
    
    Headers:
    - `device_token` (string): The session token for the user.

    Responses:
    - If the token is valid:
      - Removes the session token and logs out the user.
    - If the token is invalid:
      - Returns a `400 Bad Request` status with the message `INVALID_TOKEN`.

    Example Request:
    POST /logout-user
    Headers:
      device_token: abc123xyz

    Example Response:
    {
      "statusCode": 400,
      "message": "INVALID_TOKEN"
    }
    """
)
def logoutUser(user: UserLogout, device_token: str = Header(...)):
    if not isTokenValid(user.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    with lock: 
        sessionTokens.pop(user.username, None)

@app.get(
    "/get-user/{username}",
    summary="Get User Info",
    description="""
    Retrieves basic details for the specified user.
    
    Path Parameters:
    - `username` (string): The unique identifier for the user.

    Headers:
    - `device_token` (string): The session token for the user.

    Responses:
    - If the token is valid:
      - Returns a JSON object with the user's name, email, age, and gender.
    - If the token is invalid:
      - Returns a `400 Bad Request` status with the message `INVALID_TOKEN`.

    Example Request:
    GET /get-user/example123
    Headers:
      device_token: abc123xyz

    Example Response:
    {
      "username": "username123",
      "email": "email123@example.com",
      "firstName": "First",
      "lastName": "name",
      "age": 30,
      "gender": "M"
    }
    """
)
def getUser(username, device_token: str = Header(...)):
    logger.debug(f"Device-Token: {device_token}")
    if not isTokenValid(username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return getUserData(username)

@app.get(
    "/get-user-sessions/{username}/{type}",
    summary="Get User Sessions",
    description="""
    Retrieves the sessions the user has signed into.
    
    Path Parameters:
    - `username` (string): The unique identifier for the user.
    - `type` (string): The type of sessions to retrieve.

    Headers:
    - `device_token` (string): The session token for the user.

    Responses:
    - If the token is valid:
      - Returns a list of sessions the user has signed into.
    - If the token is invalid:
      - Returns a `400 Bad Request` status with the message `INVALID_TOKEN`.

    Example Request:
    GET /get-user-sessions/example123/previous
    Headers:
      device_token: abc123xyz

    Example Response:
    [
        {
        "id": "1",
        "name": "Pilates",
        "date": "2023-10-15",
        "hour": "10h",
        "teacher": "Example Teacher",
        "totalSpots": 20,
        "filledSpots": 15,
        "description": "A terapeutic pilates class.",
        "isActive": 0
        }
    ]
    """
)
async def get_user_sessions(username: str, type: str, device_token: str = Header(...)):
    if not isTokenValid(username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return getUserSessions(username, type)

@app.get(
    "/get-sessions/{username}",
    summary="Get Sessions",
    description="""
    Retrieves all sessions the user is not signed into.
    
    Path Parameters:
    - `username` (string): The unique identifier for the user.

    Responses:
    - Returns a list of sessions the user is not signed into.

    Example Request:
    GET /get-sessions/example123

    Example Response:
    [
        {
        "id": "1",
        "name": "Pilates",
        "date": "2023-10-15",
        "hour": "10h",
        "teacher": "Example Teacher",
        "totalSpots": 20,
        "filledSpots": 15,
        "description": "A terapeutic pilates class.",
        "isActive": 0
        }
    ]
    """
)
def getSessions(username):
  if not isTokenValid(user.username, device_token) and username != "":
      return PostResponse(statusCode=400, message="INVALID_TOKEN")
  return getSessionData(username)


@app.post(
    "/register-user",
    summary="Register User",
    description="""
    Registers a new user in the system.
    
    Request Body:
    - `username` (string): The user's username.
    - `password` (string): The user's password.
    - `email` (string): The user's email address.
    - `firstName` (string): The user's first name.
    - `lastName` (string): The user's last name.
    - `birthDay` (int): The user's birth day.
    - `birthMonth` (int): The user's birth month.
    - `birthYear` (int): The user's birth year.
    - `gender` (string): The user's gender (M/F).

    Responses:
    - If registration is successful:
      - Returns a `200 OK` status with a success message.
    - If registration fails:
      - Returns a `400 Bad Request` status with an error message.

    Example Request:
    ```json
    {
      "username": "username123",
      "password": "password123",
      "email": "email123@example.com",
      "firstName": "First",
      "lastName": "Name",
      "birthDay": 15,
      "birthMonth": 8,
      "birthYear": 1990,
      "gender": "M"
    }
    ```

    Example Response:
    {
      "statusCode": 200,
      "message": "REGISTER_OK"
    }
    """
)
def registerUser(user: RegisterUser):
    return register(user)


@app.post(
    "/heartbeat-info",
    summary="Send Heartbeat Info",
    description="""
    Sends heartbeat information for a session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.
    - `heartRate` (int): The user's heart rate (BPM).
    - `timeStamp` (int): The timestamp of the heartbeat data.

    Example Request:
    {
      "sessionId": "1",
      "username": "username123",
      "heartRate": 72,
      "timeStamp": 1698765432
    }
    """
)
async def sendHeartbeatInfo(info: HeartbeatInfo):
    await event_queue.put(await getSSEPostResponse(info.sessionId, info.username, getCurrentTimeStamp(), "HEARTRATE", str(info.heartRate)))

@app.post(
    "/hrv",
    summary="Send HRV Info",
    description="""
    Sends Heart Rate Variability (HRV) information for a session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.
    - `hrv` (int): The user's HRV value (ms).

    Example Request:
    {
      "sessionId": "1",
      "username": "username123",
      "hrv": 50
    }
    """
)
async def sendHeartbeatInfo(info: HRVInfo):
    await event_queue.put(await getSSEPostResponse(info.sessionId, info.username, getCurrentTimeStamp(), "HRV", str(info.hrv)))

@app.post(
    "/session-sign-in/",
    summary="Sign In Session",
    description="""
    Signs the user into a session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.

    Headers:
    - `device_token` (string): The session token for the user.

    Responses:
    - If the token is valid:
      - Signs the user into the session and returns a success message.
    - If the token is invalid:
      - Returns a `400 Bad Request` status with the message `INVALID_TOKEN`.

    Example Request:
    {
      "sessionId": "1",
      "username": "username123"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "SIGN_IN_OK"
    }
    """
)
def signInSession(sessionSignData: SessionSignData, device_token: str = Header(...)):
    if not isTokenValid(sessionSignData.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return saveSignInSession(sessionSignData)

@app.post(
    "/session-sign-out/",
    summary="Sign Out Session",
    description="""
    Signs the user out of a session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.

    Headers:
    - `device_token` (string): The session token for the user.

    Responses:
    - If the token is valid:
      - Signs the user out of the session and returns a success message.
    - If the token is invalid:
      - Returns a `400 Bad Request` status with the message `INVALID_TOKEN`.

    Example Request:
    {
      "sessionId": "1",
      "username": "username123"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "SIGN_OUT_OK"
    }
    """
)
def signOutSession(sessionSignData: SessionSignData, device_token: str = Header(...)):
    if not isTokenValid(sessionSignData.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return saveSignOutSession(sessionSignData)

@app.post(
    "/session-summary/",
    summary="Send Session Summary",
    description="""
    Sends a summary of the session to the server.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.
    - `measurements` (list): A list of measurements taken during the session.
    - `hrv` (int): The user's HRV value (ms).

    Headers:
    - `device_token` (string): The session token for the user.

    Example Request:
    {
      "sessionId": "1",
      "username": "username123",
      "measurements": [72, 75, 70],
      "hrv": 50
    }
    """
)
def sendSessionSummary(sessionSummaryData: SessionSummaryData, device_token: str = Header(...)):
    if not isTokenValid(sessionSummaryData.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return sendSessionSummaryData(sessionSummaryData.sessionId, sessionSummaryData.username, sessionSummaryData.measurements, sessionSummaryData.hrv)

@app.post(
    "/get-session-summary/",
    summary="Get Session Summary",
    description="""
    Retrieves the summary for a previous session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.

    Headers:
    - `device_token` (string): The session token for the user.

    Responses:
    - If the token is valid:
      - Returns the session summary.
    - If the token is invalid:
      - Returns a `400 Bad Request` status with the message `INVALID_TOKEN`.

    Example Request:
    {
      "sessionId": "1",
      "username": "username123"
    }

    Example Response:
    {
      "sessionId": "12345",
      "username": "johndoe",
      "measurements": [72, 75, 70],
      "hrv": 50
    }
    """
)
def getSessionSummary(sessionSignData: SessionSignData, device_token: str = Header(...)):
    if not isTokenValid(sessionSignData.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return getSessionSummaryData(sessionSignData)

@app.post(
    "/enter-session",
    summary="Enter Session",
    description="""
    Allows a user to enter a session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.

    Responses:
    - If the user can enter the session:
      - Returns a `200 OK` status with the message `ENTER_SESSION_OK`.
    - If the user cannot enter the session:
      - Returns a `400 Bad Request` status with the message `ENTER_SESSION_FAIL`.

    Example Request:
    {
      "sessionId": "1",
      "username": "username123"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "ENTER_SESSION_OK"
    }
    """
)
async def enterSession(sessionOperationData: SessionOperation):
    user = getUserData(sessionOperationData.username)
    if canEnterSession(sessionOperationData.sessionId) and user is not None:
        await event_queue.put(await getSSEPostResponse(sessionOperationData.sessionId, sessionOperationData.username, getCurrentTimeStamp(), "ENTER_SESSION", user.firstName))
        return PostResponse(statusCode=200, message="ENTER_SESSION_OK")
    return PostResponse(statusCode=400, message="ENTER_SESSION_FAIL")

@app.post(
    "/leave-session",
    summary="Leave Session",
    description="""
    Allows a user to leave a session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.

    Responses:
    - If the user can leave the session:
      - Returns a `200 OK` status with the message `LEAVE_SESSION_OK`.
    - If the user cannot leave the session:
      - Returns a `400 Bad Request` status with the message `LEAVE_SESSION_FAIL`.

    Example Request:
    {
      "sessionId": "1",
      "username": "username123"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "LEAVE_SESSION_OK"
    }
    """
)
async def leaveSession(sessionOperationData: SessionOperation):
    if canLeaveSession(sessionOperationData.sessionId, sessionOperationData.username):
        await event_queue.put(await getSSEPostResponse(sessionOperationData.sessionId, sessionOperationData.username, getCurrentTimeStamp(), "LEAVE_SESSION"))
        return PostResponse(statusCode=200, message="LEAVE_SESSION_OK")
    return PostResponse(statusCode=400, message="LEAVE_SESSION_FAIL")
# Password Recovery Methods. 

@app.post(
    "/send-recovery-email",
    summary="Send Recovery Email",
    description="""
    Sends a password recovery email to the user.
    
    Request Body:
    - `username` (string): The user's username.
    - `code` (int): The recovery code.
    - `languageCode` (string): The language code for the email.

    Responses:
    - If successful:
      - Returns a `200 OK` status.
    - If unsuccessful:
      - Returns a `400 Bad Request` status.

    Example Request:
    {
      "username": "username123",
      "code": 123456,
      "languageCode": "en"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "RECOVERY_EMAIL_SENT"
    }
    """
)
def sendRecoveryEmail(recoveryEmailData: RecoveryEmailData):
    return sendRecoveryEmailToUser(recoveryEmailData.username, recoveryEmailData.code, recoveryEmailData.languageCode)

@app.post(
    "/change-password",
    summary="Change Password",
    description="""
    Changes the user's password.
    
    Request Body:
    - `username` (string): The user's username.
    - `newPassword` (string): The new password.

    Responses:
    - If successful:
      - Returns a `200 OK` status.
    - If unsuccessful:
      - Returns a `400 Bad Request` status.

    Example Request:
    {
      "username": "username123",
      "newPassword": "newpassword123"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "PASSWORD_CHANGED"
    }
    """
)
def changePassword(passwordChangeData: PasswordChangeData):
    return changeUserPassword(passwordChangeData.username, passwordChangeData.newPassword)

@app.post(
    "/create-session",
    summary="Create Session",
    description="""
    Creates a new session.
    
    Request Body:
    - `teacher` (string): The teacher conducting the session.
    - `name` (string): The name of the session.
    - `description` (string): A description of the session.
    - `date` (string): The date of the session.
    - `hour` (string): The time of the session.
    - `totalSpots` (int): The total number of spots available.

    Responses:
    - If successful:
      - Returns a `200 OK` status.
    - If unsuccessful:
      - Returns a `400 Bad Request` status.

    Example Request:
    {
      "teacher": "Jane Smith",
      "name": "Morning Yoga",
      "description": "A relaxing yoga session to start your day.",
      "date": "2023-10-15",
      "hour": "10:00 AM",
      "totalSpots": 20
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "SESSION_CREATED"
    }
    """
)
def createSession(sessionCreationData: SessionCreationData):
    return createNewSession(sessionCreationData)

@app.post(
    "/login-teacher",
    summary="Login Teacher",
    description="""
    Authenticates a teacher.
    
    Request Body:
    - `name` (string): The teacher's name.
    - `password` (string): The teacher's password.

    Responses:
    - If credentials are correct:
      - Returns a `200 OK` status.
    - If credentials are incorrect:
      - Returns a `400 Bad Request` status.

    Example Request:
    {
      "name": "Example Name",
      "password": "password123"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "LOGIN_OK"
    }
    """
)
def loginTeacher(teacherLoginData: TeacherLoginData):
    return attemptTeacherLogin(teacherLoginData)

@app.post(
    "/get-teacher-sessions",
    summary="Get Teacher Sessions",
    description="""
    Retrieves sessions for a teacher.
    
    Request Body:
    - `name` (string): The teacher's name.
    - `type` (string): The type of sessions to retrieve.

    Responses:
    - If successful:
      - Returns a list of sessions.
    - If unsuccessful:
      - Returns a `400 Bad Request` status.

    Example Request:
    {
      "name": "Jane Smith",
      "type": "yoga"
    }

    Example Response:
    [
      {
        "sessionId": "12345",
        "sessionName": "Pilates clínico",
        "status": "signed"
      }
    ]
    """
)
def getTeacherSessions(teacherSessionData: TeacherSessionData):
    return searchTeacherSessions(teacherSessionData)

@app.post(
    "/cancel-session",
    summary="Cancel Session",
    description="""
    Cancels a session.
    
    Request Body:
    - `name` (string): The teacher's name.
    - `sessionId` (string): The ID of the session.

    Responses:
    - If successful:
      - Returns a `200 OK` status.
    - If unsuccessful:
      - Returns a `400 Bad Request` status.

    Example Request:
    {
      "name": "Example Name",
      "sessionId": "1"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "SESSION_CANCEL_OK"
    }
    """
)
def cancelSession(sessionCancelData: SessionCancelData):
    if attemptSessionCancel(sessionCancelData):
        return PostResponse(statusCode=200, message="SESSION_CANCEL_OK")
    return PostResponse(statusCode=400, message="SESSION_CANCEL_FAIL")

@app.post(
    "/start-session",
    summary="Start Session",
    description="""
    Starts a session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.
    - `zoomId` (string): The Zoom meeting ID.
    - `zoomPassword` (string): The Zoom meeting password.

    **Responses:**
    - If successful:
      - Returns a `200 OK` status.
    - If unsuccessful:
      - Returns a `400 Bad Request` status.

    Example Request:
    {
      "sessionId": "1",
      "zoomId": "987654321",
      "zoomPassword": "password123"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "SESSION_START_OK"
    }
    """
)
def startSession(sessionStartData: SessionStartData):
    if attemptSessionStart(sessionStartData):
        return PostResponse(statusCode=200, message="SESSION_START_OK")
    return PostResponse(statusCode=400, message="SESSION_START_FAIL")

@app.post(
    "/close-session",
    summary="Close Session",
    description="""
    Closes a session.
    
    Request Body:
    - `sessionId` (string): The ID of the session.

    Responses:
    - If successful:
      - Returns a `200 OK` status.
    - If unsuccessful:
      - Returns a `400 Bad Request` status.

    Example Request:
    {
      "sessionId": "1"
    }

    Example Response:
    {
      "statusCode": 200,
      "message": "SESSION_CLOSE_OK"
    }
    """
)
def closeSession(sessionCloseData: SessionCloseData):
    if attemptSessionClose(sessionCloseData):
        return PostResponse(statusCode=200, message="SESSION_CLOSE_OK")
    return PostResponse(statusCode=400, message="SESSION_CLOSE_FAIL")

@app.get(
    "/session/{sessionId}",
    summary="SSE Session",
    description="""
    Provides Server-Sent Events (SSE) for a session.
    
    Path Parameters:
    - `sessionId` (string): The ID of the session.

    Responses:
    - Returns a stream of events for the session.

    Example Request:
    GET /session/1

    Example Response:
    data: {"sessionId": "1", "username": "example123", "event": "HEARTRATE", "value": "72"}
    """
)
async def session(sessionId):
    return StreamingResponse(event_stream(sessionId), media_type="text/event-stream")