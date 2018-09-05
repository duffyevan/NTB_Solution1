from ftplib import FTP
import sys
import os
import datetime
import configparser
import smtplib
from SPSLib import SPSLib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from EMailLib import *
from string import Template


config = configparser.ConfigParser()
config.read('collection.conf')

addresses = (config['DEFAULT']['addresses']).split(',')
user = config['DEFAULT']['username']
password = config['DEFAULT']['password']
destination = config['DEFAULT']['default_destination']

# ftp = FTP('10.0.0.99')
# ftp.login(user=user, passwd=password)

# #file Size and days left calcualtor
# SD_size = int(config['EMAIL']['SD_size'])
# sps = SPSLib(ftp)
# tupleresult = sps.get_total_size('/')
# totalusage = tupleresult[0]
# totalusageMB = round(totalusage/(1024*1024), 2) 
# avg_size = round(totalusageMB/tupleresult[1], 2)
# size_left = round((SD_size - totalusageMB), 2)
# days_left = int(size_left/avg_size)

# print ('print tuple: ' + str(tupleresult))
# print ('Total Usage In MB: ' + str(totalusageMB) + 'MB')
# print ('Avarage file size per day in MB: ' + str(avg_size) + 'MB')
# print ('Size left before full: ' + str(size_left) + 'MB')
# print ('Days left before storage is full: ' + str(days_left) + ' days')


# sps.close_connection()


# #Emial Section:
#code used from the Website https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f

days_left = 18

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

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)



names, emails = get_contacts('email_addresses.txt') # read contacts
message_template = read_template('OneDayWarning.temp')

# set up the SMTP server
s = smtplib.SMTP(host='SMTP_SERVER', port=587)
s.starttls()
s.login(config['EMAIL']['username'],config['EMAIL']['password'])

# For each contact, send the email:
for name, email in zip(names, emails):
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(user=name.title(), address=addresses, days=days_left)

    # Prints out the message body for our sake
    print(message)

    # setup the parameters of the message
    msg['From'] = user
    msg['To'] = email
    msg['Subject'] = "This is TEST"
    
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    
    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
    
# Terminate the SMTP session and close the connection
s.quit()




# Our code for sending an email

# message = EMail(config['EMAIL']['username'], config['EMAIL']['recipient'])
# message.set_subject("Test Email Send From Library")
# message.set_body("The current SPS with the address of: 111111 has used up " + str(totalusageMB) + " MB.")

# sender = EMailSender(config['EMAIL']['smtp_server'], config['EMAIL']['smtp_port'])
# sender.login(config['EMAIL']['username'],config['EMAIL']['password'])
# sender.send_message(message)
# sender.quit()