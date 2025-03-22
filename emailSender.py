import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = "Insert your email here"
APP_PASS = "Insert your email app password here"

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
    message = MIMEMultipart()
    message['Subject'] = getRecoverySubject(languageCode, code)
    message['From'] = senderEmail
    message['To'] = receiverEmail
    message.attach(MIMEText(getRecoveryContent(languageCode, code, name), 'html'))
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
    return (
        f"<p>Olá {name}!</p>"
        f"<p>O código de recuperação de palavra-passe é: <b>{code}</b>.</p>"
        "<p>Este código tem a validade de <b>4 minutos</b>.</p>"
        "<p><b>Atenção:</b> Por segurança, não partilhe este código com ninguém.</p>"
        "<p>Se não pediu nenhum código, ignore este e-mail.</p>"
        "<p>Cumprimentos,<br>A Equipa de Suporte da HeartRateMonitoringApp</p>"
    )

def getEnglishContent(code, name):
    return (
        f"<p>Hello {name},</p>"
        f"<p>Your password recovery code is: <b>{code}</b>.</p>"
        "<p>This code is valid for <b>4 minutes</b>.</p>"
        "<p><b>Important:</b> For security reasons, do not share this code with anyone.</p>"
        "<p>If you did not request this code, please ignore this email.</p>"
        "<p>Best regards,<br>The Support Team</p>"
    )

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
    message = MIMEMultipart()
    message['Subject'] = getCancelSubject()
    message['From'] = senderEmail
    message['To'] = receiverEmail
    msg.attach(MIMEText(getCancelContent(name, session)))
    return message

# Subject
def getCancelSubject():
    return "HeartRateMonitoringApp: IMPORTANT INFORMATION"

# Content
def getCancelContent(name, session):
    return (
        f"<p>Olá {name}!</p>"
        f"<p>A sessão <b>{session.name}</b>, do dia <b>{session.date}</b> às <b>{session.hour}</b>, foi cancelada pelo professor responsável.</p>"
        "<p>Lamentamos o inconveniente e agradecemos a sua compreensão.</p>"
        "<p>Cumprimentos,<br>A Equipa de Suporte da HeartRateMonitoringApp</p>"
    )

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
    message = MIMEMultipart()
    message['Subject'] = getSessionStartSubject()
    message['From'] = senderEmail
    message['To'] = receiverEmail
    msg.attach(MIMEText(getSessionStartContent(name, session, zoomId, zoomPassword)))
    return message

# Subject
def getSessionStartSubject():
    return "HeartRateMonitoringApp: SESSION ONLINE"

# Content
def getSessionStartContent(name, session, zoomId, zoomPassword):
    return (
        f"<p>Olá {name}!</p>"
        f"<p>A sessão <b>{session.name}</b> foi iniciada pelo professor responsável. Junte-se à chamada Zoom com os dados abaixo.</p>"
        f"<p><b>ID da chamada Zoom:</b> {zoomId}</p>"
        f"<p><b>Senha da chamada Zoom:</b> {zoomPassword}</p>"
        "<p>Cumprimentos,<br>A Equipa de Suporte da HeartRateMonitoringApp</p>"
    )