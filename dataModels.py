from pydantic import BaseModel

# Data Types

class UserLogin(BaseModel):
    username: str
    password: str

class UserLogout(BaseModel):
    username: str

class RegisterUser(BaseModel):
    username: str
    password: str
    email: str
    firstName: str
    lastName: str
    birthDay: int
    birthMonth: int
    birthYear: int
    gender: str

class UserData(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    age: int
    gender: str

class HeartbeatInfo(BaseModel):
    sessionId: str
    username: str
    heartRate: int
    timeStamp: int

class Session(BaseModel):
    id: str
    name: str
    date: str
    hour: str
    teacher: str
    totalSpots: int
    filledSpots: int
    description: str
    isActive: int = 0

class SessionUsers(BaseModel):
    session: Session
    users: list[str]

class PostResponse(BaseModel):
    statusCode: int
    message: str

class LoginResponse(BaseModel):
    statusCode: int
    message: str
    deviceToken: str

class SessionSignData(BaseModel):
    username: str
    sessionId: str

class SessionSummaryData(BaseModel):
    username: str
    sessionId: str
    measurements: list = [] 

class PreviousSessionData(BaseModel):
    session: Session
    count: int
    average: int
    maximum: int
    minimum: int

class SessionOperation(BaseModel):
    username: str
    sessionId: str

class RecoveryEmailData(BaseModel):
    username: str
    code: int
    languageCode: str

class PasswordChangeData(BaseModel):
    username: str
    newPassword: str

class SessionCreationData(BaseModel):
    teacher: str
    name: str
    description: str
    date: str
    hour: str
    totalSpots: int

class TeacherLoginData(BaseModel):
    name: str
    password: str

class TeacherSessionData(BaseModel):
    name: str
    type: str

class SessionCancelData(BaseModel):
    name: str
    sessionId: str

class SessionStartData(BaseModel):
    sessionId: str
    zoomId: str
    zoomPassword: str

class SessionCloseData(BaseModel):
    sessionId: str

class SSEData(BaseModel):
    sessionId: str
    username: str
    timeStamp: str
    event: str
    value: str = ""