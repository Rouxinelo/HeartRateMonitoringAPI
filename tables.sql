-- Table to store user information
CREATE TABLE IF NOT EXISTS user (
   username TEXT PRIMARY KEY,        -- Unique identifier for the user (Primary Key)
   firstName TEXT NOT NULL,          -- User's first name
   lastName TEXT NOT NULL,           -- User's last name
   email TEXT NOT NULL,              -- User's email address
   dateOfBirth DATE NOT NULL,        -- User's date of birth (stored as TEXT)
   password TEXT NOT NULL,           -- User's password (hashed)
   gender TEXT NOT NULL              -- User's gender (M = Male, F = Female)
);

-- Table to store teacher information
CREATE TABLE IF NOT EXISTS teacher (
   username TEXT PRIMARY KEY,        -- Unique identifier for the teacher (Primary Key)
   name TEXT NOT NULL,               -- Teacher's full name
   password TEXT NOT NULL            -- Teacher's password (hashed)
);

-- Table to store session information
CREATE TABLE IF NOT EXISTS session (
   sessionId INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the session (Auto-incremented)
   name TEXT NOT NULL,                         -- Name of the session
   teacher TEXT NOT NULL,                      -- Teacher conducting the session (Foreign Key referencing teacher.username)
   description TEXT,                           -- Description of the session (optional)
   date DATE NOT NULL,                         -- Date of the session
   hour INTEGER NOT NULL,                      -- Hour of the session
   spots INTEGER NOT NULL,                      -- Number of available spots in the session
   isActive INTEGER DEFAULT 0,                 -- Indicates if the session is active (0 = inactive, 1 = active, -1 = finished)
   FOREIGN KEY (teacher) REFERENCES teacher(username) -- Relationship to the teacher table
);

-- Table to store user sign-ups for sessions
CREATE TABLE IF NOT EXISTS sessionSigning (
   sessionId INTEGER NOT NULL,                 -- Session ID (Foreign Key referencing session.sessionId)
   username TEXT NOT NULL,                     -- User's username (Foreign Key referencing user.username)
   PRIMARY KEY (sessionId, username),          -- Composite Primary Key (sessionId + username)
   FOREIGN KEY (username) REFERENCES user(username), -- Relationship to the user table
   FOREIGN KEY (sessionId) REFERENCES session(sessionId) -- Relationship to the session table
);

-- Table to store summary data for user sessions
CREATE TABLE IF NOT EXISTS sessionSummary (
   sessionId INTEGER,                          -- Session ID (Foreign Key referencing session.sessionId)
   username TEXT,                              -- User's username (Foreign Key referencing user.username)
   hrCount INTEGER,                            -- Total heart rate readings
   hrAverage INTEGER,                          -- Average heart rate during the session
   hrMaximum INTEGER,                          -- Maximum heart rate during the session
   hrMinimum INTEGER,                          -- Minimum heart rate during the session
   hrv INTEGER,                                -- Heart rate variability
   PRIMARY KEY (sessionId, username),          -- Composite Primary Key (sessionId + username)
   FOREIGN KEY (username) REFERENCES user(username), -- Relationship to the user table
   FOREIGN KEY (sessionId) REFERENCES session(sessionId) -- Relationship to the session table
);