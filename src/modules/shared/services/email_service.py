import os
import smtplib
from bs4 import BeautifulSoup
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

        content = self.prepare_template(subject, body)
        msg.attach(MIMEText(content, 'html'))

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, to, msg.as_string())

    def prepare_template(self, subject, content):
        template_path = os.path.join(os.path.dirname(
            __file__), '../templates/emails/base.html')
        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()
        template = template.replace(
            '{{subject}}', subject).replace('{{content}}', content)
        soup = BeautifulSoup(template, 'html.parser')
        return soup.prettify()
