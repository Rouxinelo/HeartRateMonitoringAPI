-- User table
CREATE TABLE IF NOT EXISTS user (
   username TEXT PRIMARY KEY,
   firstName TEXT NOT NULL,
   lastName TEXT NOT NULL,
   email TEXT NOT NULL,
   dateOfBirth TEXT NOT NULL,
   password TEXT NOT NULL,
   gender TEXT NOT NULL
);

-- Teacher table
CREATE TABLE IF NOT EXISTS teacher (
   username TEXT PRIMARY KEY,
   name TEXT NOT NULL,
   password TEXT NOT NULL
);

-- Session table with auto-incrementing sessionId
CREATE TABLE IF NOT EXISTS session (
   sessionId INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing primary key
   name TEXT NOT NULL,
   teacher TEXT NOT NULL,
   description TEXT,
   date DATE NOT NULL,
   hour INTEGER NOT NULL,
   spots INTEGER NOT NULL,
   isActive INTEGER DEFAULT 0,
   FOREIGN KEY (teacher) REFERENCES teacher(username)
);

-- SessionSigning table
CREATE TABLE IF NOT EXISTS sessionSigning (
   sessionId INTEGER NOT NULL,
   username TEXT NOT NULL,
   PRIMARY KEY (sessionId, username),
   FOREIGN KEY (username) REFERENCES user(username),
   FOREIGN KEY (sessionId) REFERENCES session(sessionId)
);

-- SessionSummary table
CREATE TABLE IF NOT EXISTS sessionSummary (
   sessionId INTEGER,
   username TEXT,
   hrCount INTEGER,
   hrAverage INTEGER,
   hrMaximum INTEGER,
   hrMinimum INTEGER,
   hrv INTEGER,
   PRIMARY KEY (sessionId, username),
   FOREIGN KEY (username) REFERENCES user(username),
   FOREIGN KEY (sessionId) REFERENCES session(sessionId)
);