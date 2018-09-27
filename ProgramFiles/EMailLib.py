from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template


## An Email Message To Be Sent Via an Email Sender 
class EMail:
    
    ## The Constructor
    # @param from_address {string} The email address to send the email from 
    # @param to_address {string} The email address to send the email to
    def __init__(self, from_address, to_address):
        self.message = MIMEMultipart()
        self.message["To"] = to_address
        self.message["From"] = from_address

    ## Set the from address
    # @param address {string} From address
    def set_from(self, address):
        
        self.message["From"] = address

    ## Set the to address
    # @param address {string} To Address
    def set_to(self, address):
        self.message["To"] = address

    ## Set the subject of the email
    # @param subject {string} The Subject
    def set_subject(self, subject):
        self.message["Subject"] = subject

    ## Set the body of the email to some text
    # @param text {string} Text to set the email body to
    def set_body(self, text):
        self.message.attach(MIMEText(text))

    ## Set the body of the emial to some html and package it up correctly
    # @param html {string} String of html code to be packaged and sent as the body
    def set_body_html(self, html):
        self.message.attach(MIMEText(html, 'html'))

    def get_from(self):
        return self.message["From"]

    def get_to(self):
        return self.message["To"]

    def get_subject(self):
        return self.message["Subject"]

    #following two functions from the Website https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f
    
    ## Returns a Template object comprising the contents of the file specified by filename.
    # @param filename {string} Path to the tempalte file to load
    # @return Template The template object to be used to construct emails
    @staticmethod
    def read_template(filename):
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    ## Return two lists names, emails containing names and email addresses read from a file specified by filename.
    # @param filename {string} Path to the tempalte file to load
    # @return (names, emails) Tuple of contact names and corresponding contact emails
    @staticmethod
    def get_contacts(filename):
        names = []
        emails = []
        with open(filename, mode='r', encoding='utf-8') as contacts_file:
            for a_contact in contacts_file:
                names.append(a_contact.split()[0])
                emails.append(a_contact.split()[1])
        return names, emails
    
    ## @var message
    # The SMTP Message object to be sent by the email sender

## Wrapper Over an SMTP Server to Send EMail Objects
class EMailSender:
    ## The Constructor
    # @param server {string} FQDN of the SMTP server
    # @param port {int} Port number for the TLS version of SMTP
    def __init__(self, server, port):
        self.smtp = smtplib.SMTP(server, port=port)
        self.smtp.starttls()

    ## Call the login function on the SMTP server
    # @param username {string} Username to use to log into the SMTP server
    # @param password {string} Password for given username    
    def login(self, username, password):
        self.smtp.login(username, password)

    ## Send a given message via the SMTP server
    # @param message {EMailLib.Email} An email object representing the message to be sent
    def send_message(self, message):
        self.smtp.sendmail(message.get_from(), message.get_to(), message.message.as_string())

    ## Quit the SMTP connection
    def quit(self):
        self.smtp.quit()



####Milap Code
    ## Setup the email object by conneting to the email server and logging in as the sender.
    # @param server_address {string} The address of the email server
    # @param server_port {string} Port number for the email server
    # @param username {string} Senders username used to log in
    # @param password {string} Senders password used to log in
    # @return sender Object with the email server connection 
    @staticmethod
    def setup_email_sender(server_address, server_port, username, password):
        sender = EMailSender(server_address, server_port)
        sender.login(username, password)
        return sender


    ## Send Warning emails for connection failer and for PLC storage being full.
    # @param sender_address {string} Senders email address
    # @param mailing_addresses {list[string, string]} List of recipients names and email addresses
    # @param templet {templet} Templet that will be used for sending emails
    # @param subject_line {string} Subject of the emails
    # @param list_sps_addresses {list[numbers]} List of PLC address
    def send_email(self, sender_address, mailing_addresses, templet, subject_line, list_sps_addresses):
        message_template = EMail.read_template(templet)
        for name, email in mailing_addresses:
            body = message_template.substitute(user=name.title(), address=list_sps_addresses)
            message = EMail(sender_address, email)
            message.set_subject(subject_line)
            message.set_body(body)
            self.send_message(message)

            # Prints out the message body for our sake
            print(body)


    ## Send Warning emails PLC storage almost full.
    # @param sender_address {string} Senders email address
    # @param mailing_addresses {list[string, string]} List of recipients names and email addresses
    # @param templet {templet} Templet that will be used for sending emails
    # @param subject_line {string} Subject of the emails
    # @param list_sps_addresses {list[numbers]} List of PLC address
    # @param warning_days {number} Warning limit before the PLC storage will be full
    def send_email_almost_full(self, sender_address, mailing_addresses, templet, subject_line, list_sps_addresses, warning_days):
        message_template = EMail.read_template(templet)
        for name, email in mailing_addresses:
            body = message_template.substitute(user=name.title(), limit=warning_days)
            addresses_string = ""
            for address, days in list_sps_addresses:
                addresses_string = addresses_string + address + " has " + str(days) + " days left.\r\n"                
            body = body.replace("[[addresses]]", addresses_string)
            message = EMail(sender_address, email)
            message.set_subject(subject_line)
            message.set_body(body)
            self.send_message(message)
            
            # Prints out the message body for our sake
            print(body)