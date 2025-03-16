# Heart Rate Monitoring API

## Overview
The Heart Rate Monitoring API is a FastAPI-based system that allows users (patients or tutors) to monitor heart rate (HR) and heart rate variability (HRV) during sessions. Users can view, sign up, and join sessions while submitting their heart data.

## Features
- User roles: Patients and Tutors
- Session management (view, sign up, create, cancel and join)
- Real-time heart rate and HRV data submission
- FastAPI-based architecture

## Installation

### 1. Clone the Project
```bash
git clone https://github.com/Rouxinelo/HeartRateMonitoringAPI.git
cd heart-rate-api
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Uvicorn
Uvicorn is required to run the FastAPI server:
```bash
pip install uvicorn
```

## Running the Server
Start the FastAPI server with the following command:
```bash
uvicorn heartRateAPI:app --host 0.0.0.0 --port 8000
```
In case performance is not as desired, you may try to run the server with more workers using the following command:
```bash
uvicorn exampleName:app --host 0.0.0.0 --port 8000 --workers X”
```
Where X is the number of workers used.
To identify the optimal number of workers you may use the following formula:

$Number Of Workers=2*Number Of CPU Cores+1$

## API Documentation
Once the server is running, access the API documentation using Redoc:
- [Redoc Documentation](http://127.0.0.1:8000/redoc)

Alternatively, you can also view the Swagger UI:
- [Swagger UI](http://127.0.0.1:8000/docs)
  
# Database Documentation

## Overview
The database is designed to store user information, session details, and heart rate data. It supports two main roles: **users** (patients) and **teachers** (tutors). Users can sign up for sessions, and their heart rate data is stored in the database for analysis.

---

## Tables

### 1. `user`
- **Description**: Stores information about users (patients).
- **Columns**:
  - `username` (TEXT, Primary Key): Unique identifier for the user.
  - `firstName` (TEXT): User's first name.
  - `lastName` (TEXT): User's last name.
  - `email` (TEXT): User's email address.
  - `dateOfBirth` (TEXT): User's date of birth.
  - `password` (TEXT): User's hashed password.
  - `gender` (TEXT): User's gender.

### 2. `teacher`
- **Description**: Stores information about teachers (tutors).
- **Columns**:
  - `username` (TEXT, Primary Key): Unique identifier for the teacher.
  - `name` (TEXT): Teacher's full name.
  - `password` (TEXT): Teacher's hashed password.

### 3. `session`
- **Description**: Stores information about sessions.
- **Columns**:
  - `sessionId` (INTEGER, Primary Key, Auto-incremented): Unique identifier for the session.
  - `name` (TEXT): Name of the session.
  - `teacher` (TEXT, Foreign Key): Teacher conducting the session (references `teacher.username`).
  - `description` (TEXT, Optional): Description of the session.
  - `date` (DATE): Date of the session.
  - `hour` (INTEGER): Hour of the session.
  - `spots` (INTEGER): Number of available spots in the session.
  - `isActive` (INTEGER, Default = 0): Indicates if the session is active (0 = inactive, 1 = active).

### 4. `sessionSigning`
- **Description**: Tracks which users have signed up for which sessions.
- **Columns**:
  - `sessionId` (INTEGER, Foreign Key): Session ID (references `session.sessionId`).
  - `username` (TEXT, Foreign Key): User's username (references `user.username`).
- **Primary Key**: Composite key (`sessionId`, `username`).

### 5. `sessionSummary`
- **Description**: Stores summary data for user sessions, including heart rate metrics.
- **Columns**:
  - `sessionId` (INTEGER, Foreign Key): Session ID (references `session.sessionId`).
  - `username` (TEXT, Foreign Key): User's username (references `user.username`).
  - `hrCount` (INTEGER): Total heart rate readings.
  - `hrAverage` (INTEGER): Average heart rate during the session.
  - `hrMaximum` (INTEGER): Maximum heart rate during the session.
  - `hrMinimum` (INTEGER): Minimum heart rate during the session.
  - `hrv` (INTEGER): Heart rate variability.
- **Primary Key**: Composite key (`sessionId`, `username`).

---

## Relationships
- **`session.teacher`** references **`teacher.username`** (Many-to-One).
- **`sessionSigning.sessionId`** references **`session.sessionId`** (Many-to-One).
- **`sessionSigning.username`** references **`user.username`** (Many-to-One).
- **`sessionSummary.sessionId`** references **`session.sessionId`** (Many-to-One).
- **`sessionSummary.username`** references **`user.username`** (Many-to-One).

---

## Example Queries
```sql
-- Get all sessions conducted by a specific teacher
SELECT * FROM session WHERE teacher = 'teacher_username';

-- Get all users signed up for a specific session
SELECT u.* FROM user u
JOIN sessionSigning ss ON u.username = ss.username
WHERE ss.sessionId = 1;

-- Get session summary for a specific user
SELECT * FROM sessionSummary WHERE username = 'user_username';

