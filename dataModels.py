from pydantic import BaseModel

# Data Types

class UserLogin(BaseModel):
    """
    Model for user login credentials.

    **Fields:**
    - `username` (string): The user's username.
    - `password` (string): The user's password.

    **Example:**
    ```json
    {
      "username": "username123",
      "password": "password123"
    }
    ```
    """
    username: str
    password: str


class UserLogout(BaseModel):
    """
    Model for user logout request.

    **Fields:**
    - `username` (string): The user's username.

    **Example:**
    ```json
    {
      "username": "username123"
    }
    ```
    """
    username: str


class RegisterUser(BaseModel):
    """
    Model for registering a new user.

    **Fields:**
    - `username` (string): The user's username.
    - `password` (string): The user's password.
    - `email` (string): The user's email address.
    - `firstName` (string): The user's first name.
    - `lastName` (string): The user's last name.
    - `birthDay` (int): The user's birth day.
    - `birthMonth` (int): The user's birth month.
    - `birthYear` (int): The user's birth year.
    - `gender` (string): The user's gender (M/F).

    **Example:**
    ```json
    {
      "username": "username123",
      "password": "password123",
      "email": "email123@example.com",
      "firstName": "First",
      "lastName": "Name",
      "birthDay": 1,
      "birthMonth": 1,
      "birthYear": 2000,
      "gender": "M"
    }
    ```
    """
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
    """
    Model for user data.

    **Fields:**
    - `username` (string): The user's username.
    - `email` (string): The user's email address.
    - `firstName` (string): The user's first name.
    - `lastName` (string): The user's last name.
    - `age` (int): The user's age.
    - `gender` (string): The user's gender (M/F).

    **Example:**
    ```json
    {
      "username": "username123",
      "email": "email123@example.com",
      "firstName": "First",
      "lastName": "Name",
      "age": 30,
      "gender": "M"
    }
    ```
    """
    username: str
    email: str
    firstName: str
    lastName: str
    age: int
    gender: str


class HeartbeatInfo(BaseModel):
    """
    Model for Heart Rate (HR) information.

    **Fields:**
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.
    - `heartRate` (int): The user's heart rate (BPM).
    - `timeStamp` (int): The timestamp of the heartbeat data.

    **Example:**
    ```json
    {
      "sessionId": "1",
      "username": "example123",
      "heartRate": 72,
      "timeStamp": 1698765432
    }
    ```
    """
    sessionId: str
    username: str
    heartRate: int
    timeStamp: int


class HRVInfo(BaseModel):
    """
    Model for Heart Rate Variability (HRV) information.

    **Fields:**
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.
    - `hrv` (int): The user's HRV value (ms).

    **Example:**
    ```json
    {
      "sessionId": "1",
      "username": "example123",
      "hrv": 50
    }
    ```
    """
    sessionId: str
    username: str
    hrv: int


class Session(BaseModel):
    """
    Model for a session.

    **Fields:**
    - `id` (string): The ID of the session.
    - `name` (string): The name of the session.
    - `date` (string): The date of the session.
    - `hour` (string): The time of the session.
    - `teacher` (string): The teacher conducting the session.
    - `totalSpots` (int): The total number of spots available.
    - `filledSpots` (int): The number of spots filled.
    - `description` (string): A description of the session.
    - `isActive` (int, optional): Indicates if the session is active (default: 0, unactive).

    **Example:**
    ```json
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
    ```
    """
    id: str
    name: str
    date: str
    hour: str
    teacher: str
    totalSpots: int
    filledSpots: int
    description: str
    isActive: int = 0


class PostResponse(BaseModel):
    """
    Model for a generic API response.

    **Fields:**
    - `statusCode` (int): The HTTP status code.
    - `message` (string): A message describing the result.

    **Example:**
    ```json
    {
      "statusCode": 200,
      "message": "LOGIN_OK"
    }
    ```
    """
    statusCode: int
    message: str


class LoginResponse(BaseModel):
    """
    Model for a login response.

    **Fields:**
    - `statusCode` (int): The HTTP status code.
    - `message` (string): A message describing the result.
    - `deviceToken` (string): A token generated for the session.

    **Example:**
    ```json
    {
      "statusCode": 200,
      "message": "LOGIN_OK",
      "deviceToken": "abc123xyz"
    }
    ```
    """
    statusCode: int
    message: str
    deviceToken: str


class SessionSignData(BaseModel):
    """
    Model for session sign-in/sign-out data.

    **Fields:**
    - `username` (string): The user's username.
    - `sessionId` (string): The ID of the session.

    **Example:**
    ```json
    {
      "username": "username123",
      "sessionId": "1"
    }
    ```
    """
    username: str
    sessionId: str


class SessionSummaryData(BaseModel):
    """
    Model for session summary data.

    **Fields:**
    - `username` (string): The user's username.
    - `sessionId` (string): The ID of the session.
    - `measurements` (list): A list of measurements taken during the session.
    - `hrv` (int): The user's HRV value.

    **Example:**
    ```json
    {
      "username": "username123",
      "sessionId": "1",
      "measurements": [72, 75, 70],
      "hrv": 50
    }
    ```
    """
    username: str
    sessionId: str
    measurements: list = []
    hrv: int


class PreviousSessionData(BaseModel):
    """
    Model for data about a previous session.

    **Fields:**
    - `session` (Session): The session details.
    - `count` (int): The number of measurements taken.
    - `average` (int): The average measurement value.
    - `maximum` (int): The maximum measurement value.
    - `minimum` (int): The minimum measurement value.
    - `hrv` (int): The user's HRV value.

    **Example:**
    ```json
    {
      "session": {
        "id": "1",
        "name": "Pilates",
        "date": "20-10-2000",
        "hour": "10h",
        "teacher": "Example Name",
        "totalSpots": 20,
        "filledSpots": 15,
        "description": "A terapeutic pilates class.",
        "isActive": -1
      },
      "count": 3,
      "average": 72,
      "maximum": 75,
      "minimum": 70,
      "hrv": 50
    }
    ```
    """
    session: Session
    count: int
    average: int
    maximum: int
    minimum: int
    hrv: int


class SessionOperation(BaseModel):
    """
    Model for session operations (e.g., entering or leaving a session).

    **Fields:**
    - `username` (string): The user's username.
    - `sessionId` (string): The ID of the session.

    **Example:**
    ```json
    {
      "username": "username123",
      "sessionId": "1"
    }
    ```
    """
    username: str
    sessionId: str


class RecoveryEmailData(BaseModel):
    """
    Model for password recovery email data.

    **Fields:**
    - `username` (string): The user's username.
    - `code` (int): The recovery code.
    - `languageCode` (string): The language code for the email.

    **Example:**
    ```json
    {
      "username": "username123",
      "code": 123456,
      "languageCode": "en"
    }
    ```
    """
    username: str
    code: int
    languageCode: str


class PasswordChangeData(BaseModel):
    """
    Model for password change data.

    **Fields:**
    - `username` (string): The user's username.
    - `newPassword` (string): The new password.

    **Example:**
    ```json
    {
      "username": "username123",
      "newPassword": "newpassword123"
    }
    ```
    """
    username: str
    newPassword: str


class SessionCreationData(BaseModel):
    """
    Model for session creation data.

    **Fields:**
    - `teacher` (string): The teacher conducting the session.
    - `name` (string): The name of the session.
    - `description` (string): A description of the session.
    - `date` (string): The date of the session.
    - `hour` (string): The time of the session.
    - `totalSpots` (int): The total number of spots available.

    **Example:**
    ```json
    {
      "teacher": "Example name",
      "name": Pilates",
      "description": "A terapeutic pilates class.",
      "date": "20-10-2000",
      "hour": "10h",
      "totalSpots": 20
    }
    ```
    """
    teacher: str
    name: str
    description: str
    date: str
    hour: str
    totalSpots: int


class TeacherLoginData(BaseModel):
    """
    Model for teacher login data.

    **Fields:**
    - `name` (string): The teacher's name.
    - `password` (string): The teacher's password.

    **Example:**
    ```json
    {
      "name": "Example Name",
      "password": "password123"
    }
    ```
    """
    name: str
    password: str


class TeacherSessionData(BaseModel):
    """
    Model for teacher session data.

    **Fields:**
    - `name` (string): The teacher's name.
    - `type` (string): The type of session (joinable, previous or signed).

    **Example:**
    ```json
    {
      "name": "Example Name",
      "type": "joinable"
    }
    ```
    """
    name: str
    type: str


class SessionCancelData(BaseModel):
    """
    Model for session cancellation data.

    **Fields:**
    - `name` (string): The teacher's name.
    - `sessionId` (string): The ID of the session to cancel.

    **Example:**
    ```json
    {
      "name": "Example Name",
      "sessionId": "1"
    }
    ```
    """
    name: str
    sessionId: str


class SessionStartData(BaseModel):
    """
    Model for session start data.

    **Fields:**
    - `sessionId` (string): The ID of the session.
    - `zoomId` (string): The Zoom meeting ID.
    - `zoomPassword` (string): The Zoom meeting password.

    **Example:**
    ```json
    {
      "sessionId": "1",
      "zoomId": "123456789",
      "zoomPassword": "password123"
    }
    ```
    """
    sessionId: str
    zoomId: str
    zoomPassword: str


class SessionCloseData(BaseModel):
    """
    Model for session close data.

    **Fields:**
    - `sessionId` (string): The ID of the session.

    **Example:**
    ```json
    {
      "sessionId": "1"
    }
    ```
    """
    sessionId: str


class SSEData(BaseModel):
    """
    Model for Server-Sent Events (SSE) data.

    **Fields:**
    - `sessionId` (string): The ID of the session.
    - `username` (string): The user's username.
    - `timeStamp` (string): The timestamp of the event.
    - `event` (string): The type of event.
    - `value` (string, optional): Additional data for the event.

    **Example:**
    ```json
    {
      "sessionId": "1",
      "username": "username123",
      "timeStamp": "10000",
      "event": "HEARTRATE",
      "value": "72"
    }
    ```
    """
    sessionId: str
    username: str
    timeStamp: str
    event: str
    value: str = ""