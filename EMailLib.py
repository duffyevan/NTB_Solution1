from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template



class EMail:
    """An Email Message To Be Sent Via an Email Sender
    """

    def __init__(self, from_address, to_address):
        """The Constructor
        
        Arguments:
            from_address {string} -- The email address to send the email from 
            to_address {string} -- The email address to send the email to
        """
        self.message = MIMEMultipart()
        self.message["To"] = to_address
        self.message["From"] = from_address

    def set_from(self, address):
        """Set the from address
        
        Arguments:
            address {string} -- From address
        """
        self.message["From"] = address

    def set_to(self, address):
        """Set the to address
        
        Arguments:
            address {string} -- To Address
        """

        self.message["To"] = address

    def set_subject(self, subject):
        """Set the subject of the email
        
        Arguments:
            subject {string} -- The Subject
        """

        self.message["Subject"] = subject

    def set_body(self, text):
        """Set the body of the email to some text
        
        Arguments:
            text {string} -- Text to set the email body to
        """

        self.message.attach(MIMEText(text))

    def set_body_html(self, html):
        """Set the body of the emial to some html and package it up correctly
        
        Arguments:
            html {string} -- String of html code to be packaged and sent as the body
        """

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
        """Returns a Template object comprising the contents of the 
        file specified by filename.

        Arguments:
            filename {string} -- Path to the tempalte file to load

        Returns:
            Template -- The template object to be used to construct emails
        """
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    @staticmethod
    def get_contacts(filename):
        """Return two lists names, emails containing names and email addresses
        read from a file specified by filename.
        
        Arguments:
            filename {string} -- Path to the tempalte file to load

        Returns:
            (names, emails) -- Tuple of contact names and corresponding contact emails
        """
        
        names = []
        emails = []
        with open(filename, mode='r', encoding='utf-8') as contacts_file:
            for a_contact in contacts_file:
                names.append(a_contact.split()[0])
                emails.append(a_contact.split()[1])
        return names, emails


class EMailSender:
    """Wrapper Over an SMTP Server to Send EMail Objects
    """

    def __init__(self, server, port):
        """The Constructor
        
        Arguments:
            server {string} -- FQDN of the SMTP server
            port {int} -- Port number for the TLS version of SMTP
        """

        self.smtp = smtplib.SMTP(server, port=port)
        self.smtp.starttls()
    
    def login(self, username, password):
        """Call the login function on the SMTP server
        
        Arguments:
            username {string} -- Username to use to log into the SMTP server
            password {string} -- Password for given username
        """

        self.smtp.login(username, password)

    def send_message(self, message):
        """Send a given message via the SMTP server
        
        Arguments:
            message {EMailLib.Email} -- An email object representing the message to be sent
        """

        self.smtp.sendmail(message.get_from(), message.get_to(), message.message.as_string())

    def quit(self):
        """Quit the SMTP connection
        """

        self.smtp.quit()
