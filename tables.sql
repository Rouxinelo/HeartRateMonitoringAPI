CREATE TABLE IF NOT EXISTS user (
   username TEXT PRIMARY KEY,
   firstName TEXT NOT NULL,
   lastName TEXT NOT NULL,
   email TEXT NOT NULL,
   dateOfBirth TEXT NOT NULL,
   password TEXT NOT NULL,
   gender TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS teacher (
   name TEXT PRIMARY KEY,
   password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS session (
   sessionId INTEGER PRIMARY KEY,
   name TEXT NOT NULL,
   teacher TEXT NOT NULL,
   description TEXT,
   date DATE NOT NULL,
   hour INTEGER NOT NULL,
   spots INTEGER NOT NULL,
   isActive INTEGER DEFAULT 0,
   FOREIGN KEY (teacher) REFERENCES teacher(name)
);

CREATE TABLE IF NOT EXISTS sessionSigning (
   sessionId INTEGER NOT NULL,
   username TEXT NOT NULL,
   PRIMARY KEY (sessionId, username),
   FOREIGN KEY (username) REFERENCES user(username),
   FOREIGN KEY (sessionId) REFERENCES session(sessionId)
);

CREATE TABLE IF NOT EXISTS sessionData (
   sessionId INTEGER,
   username TEXT,
   timestamp TEXT,
   heartRate INTEGER,
   PRIMARY KEY (sessionId, username, timestamp),
   FOREIGN KEY (username) REFERENCES user(username),
   FOREIGN KEY (sessionId) REFERENCES session(sessionId)
);

CREATE TABLE IF NOT EXISTS sessionSummary (
   sessionId INTEGER,
   username TEXT,
   count INTEGER,
   average INTEGER,
   maximum INTEGER,
   minimum INTEGER,
   PRIMARY KEY (sessionId, username),
   FOREIGN KEY (username) REFERENCES user(username),
   FOREIGN KEY (sessionId) REFERENCES session(sessionId)
);
