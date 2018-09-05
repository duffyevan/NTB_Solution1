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
import time


config = configparser.ConfigParser()
config.read('collection.conf')

addresses = (config['DEFAULT']['addresses']).split(',')
user = config['DEFAULT']['username']
password = config['DEFAULT']['password']
destination = config['DEFAULT']['default_destination']
numretries = int(config['DEFAULT']['number_connection_retries'])
retrydelay = int(config['DEFAULT']['connection_retry_delay'])

ftp = 0
for address in addresses:
    success = False
    for n in range(0, numretries):
        try:
            ftp = FTP(address)
            ftp.login(user=user, passwd=password)
            success = True
        except:
            print('Connection Attempt ' + str(n+1) + ' to ' + address + ' Failed')
            time.sleep(retrydelay)

    if not success:
        print('Error Connecting To PLC at ' + address)
        continue
        # sys.exit(1)



    #file Size and days left calcualtor
    SD_size = int(config['EMAIL']['SD_size'])
    sps = SPSLib(ftp)
    tupleresult = sps.get_total_size('/')
    totalusage = tupleresult[0]
    totalusageMB = round(totalusage/(1024*1024), 2) 
    avg_size = round(totalusageMB/tupleresult[1], 2)
    size_left = round((SD_size - totalusageMB), 2)
    days_left = int(size_left/avg_size)

    print ('print tuple: ' + str(tupleresult))
    print ('Total Usage In MB: ' + str(totalusageMB) + 'MB')
    print ('Avarage file size per day in MB: ' + str(avg_size) + 'MB')
    print ('Size left before full: ' + str(size_left) + 'MB')
    print ('Days left before storage is full: ' + str(days_left) + ' days')


    sps.close_connection()


    #Emial Section:

    names, emails = EMail.get_contacts('email_templates/email_addresses.txt') # read contacts
    message_template = EMail.read_template('email_templates/OneDayWarning.temp')


    sender = EMailSender(config['EMAIL']['smtp_server'], config['EMAIL']['smtp_port'])
    sender.login(config['EMAIL']['username'],config['EMAIL']['password'])

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        body = message_template.substitute(user=name.title(), address=address, days=days_left)
        
        message = EMail(config['EMAIL']['username'], email)
        message.set_subject("Test Email Send From Library")
        message.set_body(body)

        # send the message via the server set up earlier.
        # sender.send_message(message)

        # Prints out the message body for our sake
        print(body)
        
    # Terminate the SMTP session and close the connection
    sender.quit()