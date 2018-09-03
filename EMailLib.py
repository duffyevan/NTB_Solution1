from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class EMail:
    def __init__(self, from_address, to_address):
        self.message = MIMEMultipart()
        self.message["To"] = to_address
        self.message["From"] = from_address

    def set_from(self, address):
        self.message["From"] = address

    def set_to(self, address):
        self.message["To"] = address

    def set_subject(self, subject):
        self.message["Subject"] = subject

    def set_body(self, text):
        self.message.attach(MIMEText(text))

    def set_body_html(self, html):
        self.message.attach(MIMEText(html, 'html'))

    def get_from(self):
        return self.message["From"]

    def get_to(self):
        return self.message["To"]

    def get_subject(self):
        return self.message["Subject"]


class EMailSender:
    def __init__(self, server, port):
        self.smtp = smtplib.SMTP(server, port=port)
        self.smtp.starttls()
    
    def login(self, username, password):
        self.smtp.login(username, password)

    def send_message(self, message):
        self.smtp.sendmail(message.get_from(), message.get_to(), message.message.as_string())

    def quit(self):
        self.smtp.quit()
