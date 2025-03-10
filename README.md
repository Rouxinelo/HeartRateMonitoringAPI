# Heart Rate Monitoring API

## Overview
The Heart Rate Monitoring API is a FastAPI-based system that allows users (patients or tutors) to monitor heart rate (HR) and heart rate variability (HRV) during sessions. Users can view, sign up, and join sessions while submitting their heart data.

## Features
- User roles: Patients and Tutors
- Session management (view, sign up, and join)
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

## API Documentation
Once the server is running, access the API documentation using Redoc:
- [Redoc Documentation](http://127.0.0.1:8000/redoc)

Alternatively, you can also view the Swagger UI:
- [Swagger UI](http://127.0.0.1:8000/docs)
  
---
Feel free to modify and improve the project. Contributions are welcome!

