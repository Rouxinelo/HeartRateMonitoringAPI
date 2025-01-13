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

# Main Path, Unavailable

@app.get("/")
def index(): 
    return {"path": "Invalid Path"}

# Login Path. Used to login to the system

@app.post("/login-user")
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

# Logout Path. Used to logout

@app.post("/logout-user")
def logoutUser(user: UserLogout, device_token: str = Header(...)):
    if not isTokenValid(user.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    logger.debug(f"Device-Token: {device_token}")
    with lock: 
        sessionTokens.pop(user.username, None)

# Get User Data Path. Used to get the user's Data after login

@app.get("/get-user/{username}")
def getUser(username, device_token: str = Header(...)):
    logger.debug(f"Device-Token: {device_token}")
    if not isTokenValid(username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return getUserData(username)

# User Sessions Path. Used to get the sessions a user signed in
@app.get("/get-user-sessions/{username}/{type}")
async def get_user_sessions(username: str, type: str, device_token: str = Header(...)):
    if not isTokenValid(username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return getUserSessions(username, type)

# Get Sessions Path. Used to get all the sessions a user is not signed in 
@app.get("/get-sessions/{username}")
def getSessions(username):
    return getSessionData(username)

# Register Path. Used to Register a new user in the system

@app.post("/register-user")
def registerUser(user: RegisterUser):
    return register(user)

# Send HeartBeat Info Path.

@app.post("/heartbeat-info")
async def sendHeartbeatInfo(info: HeartbeatInfo):
    await event_queue.put(await getSSEPostResponse(info.sessionId, info.username, getCurrentTimeStamp(), "HEARTRATE", str(info.heartRate)))
    return saveHeartbeatInfo(info)

# Sign in session 
@app.post("/session-sign-in/")
def signInSession(sessionSignData: SessionSignData, device_token: str = Header(...)):
    if not isTokenValid(username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return saveSignInSession(sessionSignData)

# Sign out session
@app.post("/session-sign-out/")
def signOutSession(sessionSignData: SessionSignData, device_token: str = Header(...)):
    if not isTokenValid(sessionSignData.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return saveSignOutSession(sessionSignData)

# Session summary. Used to send the session summary to the server
@app.post("/session-summary/")
def sendSessionSummary(sessionSummaryData: SessionSummaryData, device_token: str = Header(...)):
    if not isTokenValid(sessionSummaryData.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return sendSessionSummaryData(sessionSummaryData.sessionId, sessionSummaryData.username, sessionSummaryData.measurements)

# Get Session Summary. Used to get the session summary for a previous session
@app.post("/get-session-summary/")
def getSessionSummary(sessionSignData: SessionSignData, device_token: str = Header(...)):
    if not isTokenValid(sessionSignData.username, device_token):
        return PostResponse(statusCode=400, message="INVALID_TOKEN")
    return getSessionSummaryData(sessionSignData)

# Get Session Operation. Used to see if user logs in or out of a session 

@app.post("/enter-session")
async def enterSession(sessionOperationData: SessionOperation):
    user = getUserData(sessionOperationData.username)
    if canEnterSession(sessionOperationData.sessionId) and user is not None:
        await event_queue.put(await getSSEPostResponse(sessionOperationData.sessionId, sessionOperationData.username, getCurrentTimeStamp(), "ENTER_SESSION", user.firstName))
        return PostResponse(statusCode=200, message="ENTER_SESSION_OK")
    return PostResponse(statusCode=400, message="ENTER_SESSION_FAIL")


@app.post("/leave-session")
async def leaveSession(sessionOperationData: SessionOperation):
    if canLeaveSession(sessionOperationData.sessionId, sessionOperationData.username):
        await event_queue.put(await getSSEPostResponse(sessionOperationData.sessionId, sessionOperationData.username, getCurrentTimeStamp(), "LEAVE_SESSION"))
        return PostResponse(statusCode=200, message="LEAVE_SESSION_OK")
    return PostResponse(statusCode=400, message="LEAVE_SESSION_FAIL")

# Password Recovery Methods. 

@app.post("/send-recovery-email")
def sendRecoveryEmail(recoveryEmailData: RecoveryEmailData):
    return sendRecoveryEmailToUser(recoveryEmailData.username, recoveryEmailData.code, recoveryEmailData.languageCode)

@app.post("/change-password")
def changePassword(passwordChangeData: PasswordChangeData):
    return changeUserPassword(passwordChangeData.username, passwordChangeData.newPassword)

# Session Creation Methods

@app.post("/create-session")
def createSession(sessionCreationData: SessionCreationData):
    return createNewSession(sessionCreationData)

@app.post("/login-teacher")
def loginTeacher(teacherLoginData: TeacherLoginData):
    return attemptTeacherLogin(teacherLoginData)

# Session Checking Methods

@app.post("/get-teacher-sessions")
def getTeacherSessions(teacherSessionData: TeacherSessionData):
    return searchTeacherSessions(teacherSessionData)

# Session Cancel Methods

@app.post("/cancel-session")
def cancelSession(sessionCancelData: SessionCancelData):
    if attemptSessionCancel(sessionCancelData):
        return PostResponse(statusCode=200, message="SESSION_CANCEL_OK")
    return PostResponse(statusCode=400, message="SESSION_CANCEL_FAIL")

# Start Session Methods

@app.post("/start-session")
def startSession(sessionStartData: SessionStartData):
    if attemptSessionStart(sessionStartData):
        return PostResponse(statusCode=200, message="SESSION_START_OK")
    return PostResponse(statusCode=400, message="SESSION_START_FAIL")

# Session Close Methods
@app.post("/close-session")
def closeSession(sessionCloseData: SessionCloseData):
    if attemptSessionClose(sessionCloseData):
        return PostResponse(statusCode=200, message="SESSION_CLOSE_OK")
    return PostResponse(statusCode=400, message="SESSION_CLOSE_FAIL")

# SSE Methods (For Session handling by the teacher)
@app.get("/session/{sessionId}")
async def session(sessionId):
    return StreamingResponse(event_stream(sessionId), media_type="text/event-stream")

async def event_stream(sessionId):
    while True:
        data = await event_queue.get()
        if data.sessionId == sessionId:
            yield data.json()


# SSE Methods (For Session handling by the teacher)
@app.get("/testEnter/{sessionId}/{username}")
async def example(sessionId, username):
    await event_queue.put(await getSSEPostResponse(sessionId, username, getCurrentTimeStamp(), "ENTER_SESSION", username))

@app.get("/testLeave/{sessionId}")
async def example(sessionId):
    await event_queue.put(await getSSEPostResponse(sessionId, "testUsername", getCurrentTimeStamp(), "LEAVE_SESSION"))

@app.get("/testHeart/{sessionId}")
async def example(sessionId):
    await event_queue.put(await getSSEPostResponse(sessionId, "1", getCurrentTimeStamp(), "HEARTRATE", f'{random.randint(80, 120)}'))