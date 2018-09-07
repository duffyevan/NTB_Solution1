from ftplib import FTP
import sys
import os
import datetime
import configparser
import smtplib
from SPSLib import SPSLib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from EMailLib import EMail, EMailSender
from HostpointLib import HostpointClient
import time


config = configparser.ConfigParser()
config.read('collection.conf')

addresses = (config['DEFAULT']['addresses']).split(',')
user = config['DEFAULT']['username']
password = config['DEFAULT']['password']
destination = config['DEFAULT']['default_destination']
numretries = int(config['DEFAULT']['number_connection_retries'])
retrydelay = int(config['DEFAULT']['connection_retry_delay'])
warning_days = int(config['EMAIL']['warning_days'])

failed_connections = []
days_rem = []
full_plcs = []

for address in addresses:
    success = False
    ftp = 0
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
        failed_connections.append(address)
        continue



    #file Size and days left calcualtor
    SD_size = int(config['EMAIL']['SD_size'])
    sps = SPSLib(ftp, default_destination=destination)
    tupleresult = sps.get_total_size('/')
    totalusage = tupleresult[0]
    totalusageMB = round(totalusage/(1024*1024), 2) 
    avg_size = round(totalusageMB/tupleresult[1], 2)
    size_left = round((SD_size - totalusageMB), 2)
    days_left = int(size_left/avg_size)
    if days_left <= warning_days and days_left > 0:
        days_rem.append((address, days_left))
    elif days_left is 0:
        full_plcs.append(address)

    files_before_download = os.listdir(destination) # list out the target dir to get the list of old files
    print("Downloading Files From SPS...")
    sps.download_files_for_month(datetime.datetime.now()) # download all files from the month
    print("Done!")
    files_after_download = os.listdir(destination) # get the new list of files 
    new_files = list(set(files_after_download) - set(files_before_download)) # isolate a list of files that are newly downloaded
    print("Uploading Files To HostPoint...")
    hp = HostpointClient(config['HOSTPOINT']['hostname'],config['HOSTPOINT']['username'],config['HOSTPOINT']['password']) # Log into the hostpoint ftp server
    hp.upload_files([os.path.join(destination, file) for file in new_files]) # Upload only the new files that have just been downloaded
    print("Done!")

    sps.close_connection()




"""
Send Warning Emails
"""

names, emails = EMail.get_contacts('email_templates/email_addresses.txt') # read contacts

sender = EMailSender(config['EMAIL']['smtp_server'], config['EMAIL']['smtp_port'])
sender.login(config['EMAIL']['username'],config['EMAIL']['password'])

if len(failed_connections) > 0:
    # For each contact, send the email:
    message_template = EMail.read_template('email_templates/ConnectionError.temp')
    for name, email in zip(names, emails):

        # add in the actual person name to the message template
        body = message_template.substitute(user=name.title(), address=failed_connections)
        
        message = EMail(config['EMAIL']['username'], email)
        message.set_subject("SPS Connection Error")
        message.set_body(body)

        # send the message via the server set up earlier.
        sender.send_message(message)

        # Prints out the message body for our sake
        print(body)

if len(full_plcs) > 0:
    # For each contact, send the email:
    message_template = EMail.read_template('email_templates/SPS_FullWarning.temp')
    for name, email in zip(names, emails):

        # add in the actual person name to the message template
        body = message_template.substitute(user=name.title(), address=full_plcs)
        
        message = EMail(config['EMAIL']['username'], email)
        message.set_subject("SPSs Are Full")
        message.set_body(body)

        # send the message via the server set up earlier.
        sender.send_message(message)

        # Prints out the message body for our sake
        print(body)

if len(days_rem) > 0:
    # For each contact, send the email:
    message_template = EMail.read_template('email_templates/DaysLeftWarning.temp')
    for name, email in zip(names, emails):

        # add in the actual person name to the message template
        body = message_template.substitute(user=name.title(), address=full_plcs, limit=config['EMAIL']['warning_days'])
        
        addresses_string = ""
        for address, days in days_rem:
            addresses_string = addresses_string + address + " has " + str(days) + " days left.\r\n" 

        body = body.replace("[[addresses]]", addresses_string)

        message = EMail(config['EMAIL']['username'], email)
        message.set_subject("SPSs Are Almost Full")
        message.set_body(body)

        # send the message via the server set up earlier.
        sender.send_message(message)

        # Prints out the message body for our sake
        print(body)

# Terminate the SMTP session and close the connection
sender.quit()
