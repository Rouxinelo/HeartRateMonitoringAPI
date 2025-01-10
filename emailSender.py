import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

EMAIL = "heartRateMonitoringAppEvora@gmail.com"
APP_PASS = "hqoletnboermlyxf"

############## Email Recovery Methods ##############
def sendRecoveryEmail(senderEmail, appLoginCode, receiverEmail, code, languageCode, name):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(senderEmail, appLoginCode)
    try:
        server.send_message(getRecoveryMessage(senderEmail, receiverEmail, code, languageCode, name))
        return 1
    except Exception as e:
        return 0

# Message
def getRecoveryMessage(senderEmail, receiverEmail, code, languageCode, name):
    message = EmailMessage()
    message['Subject'] = getRecoverySubject(languageCode, code)
    message['From'] = senderEmail
    message['To'] = receiverEmail
    message.set_content(getRecoveryContent(languageCode, code, name))
    return message

# Subject
def getRecoverySubject(languageCode, code):
    if languageCode == "en":
        return getEnglishSubject()
    return getPortugueseSubject()

def getPortugueseSubject():
    return "O seu codigo de recuperação para a sua conta HeartRateMonitoringApp"

def getEnglishSubject():
    return "Your HeartRateMonitoringApp password recovery code"

# Content
def getRecoveryContent(languageCode, code, name):
    if languageCode == "En":
        return getEnglishContent(code, name)
    return getPortugueseContent(code, name)

def getPortugueseContent(code, name):
    return f'Olá {name}.\nO codigo de recuperação de palavra passe é {code}.\nNão partilho o código com ninguém, e se não o pediu, ignore o mesmo.'

def getEnglishContent(code, name):
    return f'Hello {name}.\nThe password recovery code you requested is {code}.\nDo not share this code with anyone, and if you did not request it, ignore this email.'

############## Session Canceled Email ##############
def sendCancelationEmail(senderEmail, appLoginCode, receiverEmail, name, session):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(senderEmail, appLoginCode)
    try:
        server.send_message(getCancelMessage(senderEmail, receiverEmail, name, session))
        return 1
    except Exception as e:
        return 0

# Message
def getCancelMessage(senderEmail, receiverEmail, name, session):
    message = EmailMessage()
    message['Subject'] = getCancelSubject()
    message['From'] = senderEmail
    message['To'] = receiverEmail
    message.set_content(getCancelContent(name, session))
    return message

# Subject
def getCancelSubject():
    return "HeartRateMonitoringApp: IMPORTANT INFORMATION"

# Content
def getCancelContent(name, session):
    return f'PT: Olá {name}!\nA sessão {session.name}, do dia {session.date} às {session.hour} foi cancelada pelo professor responsável.\n\nEN: Hello {name}!\nThe session {session.name}, scheduled for {session.date} at {session.hour} was canceled by its responsible teacher.'

############## Session Start Email ##############
def sendSessionStartEmail(senderEmail, appLoginCode, receiverEmail, name, session, zoomId, zoomPassword):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(senderEmail, appLoginCode)
    try:
        server.send_message(getSessionStartMessage(senderEmail, receiverEmail, name, session, zoomId, zoomPassword))
        return 1
    except Exception as e:
        return 0 

# Message
def getSessionStartMessage(senderEmail, receiverEmail, name, session, zoomId, zoomPassword):
    message = EmailMessage()
    message['Subject'] = getSessionStartSubject()
    message['From'] = senderEmail
    message['To'] = receiverEmail
    message.set_content(getSessionStartContent(name, session, zoomId, zoomPassword))
    return message

# Subject
def getSessionStartSubject():
    return "HeartRateMonitoringApp: SESSION ONLINE"

# Content
def getSessionStartContent(name, session, zoomId, zoomPassword):
    return f'PT: Olá {name}!\nA sessão {session.name}  foi iniciada pelo professor responsável. Junte-se à chamada Zoom com os dados abaixo.\n\nEN: Hello {name}!\nThe session {session.name} was started by its responsible teacher. Join the Zoom call listed below. \n\n\nZoom Call Id: {zoomId}\nZoom Call Password: {zoomPassword}'
