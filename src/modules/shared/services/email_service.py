import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    def __init__(self, **EMAIL_SMTP):
        self.smtp_server = EMAIL_SMTP["SERVER"]
        self.port = EMAIL_SMTP["PORT"]
        self.username = EMAIL_SMTP["USERNAME"]
        self.password = EMAIL_SMTP["PASSWORD"]

    def send_email(self, to, subject, body):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to

        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, to, msg.as_string())
