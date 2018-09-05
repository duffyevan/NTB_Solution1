from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template



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

    #following two functions from the Website https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f

    @staticmethod
    def read_template(filename):
        """
        Returns a Template object comprising the contents of the 
        file specified by filename.
        """
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    @staticmethod
    def get_contacts(filename):
        """
        Return two lists names, emails containing names and email addresses
        read from a file specified by filename.
        """
        
        names = []
        emails = []
        with open(filename, mode='r', encoding='utf-8') as contacts_file:
            for a_contact in contacts_file:
                names.append(a_contact.split()[0])
                emails.append(a_contact.split()[1])
        return names, emails


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
