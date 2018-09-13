from ftplib import FTP
import sys
import os
import datetime
import configparser
import smtplib
from SPSLib import SPSLib, SPSConnectionException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from EMailLib import EMail, EMailSender
from HostpointLib import HostpointClient
import time


#setup reading the config file
config = configparser.ConfigParser()
config.read('collection.conf')

#set the veriables according to the config file
addresses = (config['DEFAULT']['addresses']).split(',')
user = config['DEFAULT']['username']
password = config['DEFAULT']['password']
destination = config['DEFAULT']['default_destination'].replace("~", "c:\\Users\\" + os.getlogin())
numretries = int(config['DEFAULT']['number_connection_retries'])
retrydelay = int(config['DEFAULT']['connection_retry_delay'])
warning_days = int(config['EMAIL']['warning_days'])

#list veriables that will be used for email perposes
failed_connections = []
days_rem = []
full_plcs = []

#check to see of a download folder exists for the given path on the pc
SPSLib.path_exist(destination)


#For each plc address, do the following 
for address in addresses:
    
    #Check to see if a folder exists for the given plc address on the local pc
    plc_dest = plc_dest = (destination + address + '\\')
    SPSLib.path_exist(plc_dest)

    #log in to the plc via ftp
    try:
        sps = SPSLib(address, user, password, default_destination=destination, numretries=numretries, retrydelay=retrydelay)
    except SPSConnectionException as ex:
        failed_connections.append(address)
        continue

    #finds days left before sps is full
    days_left = sps.calulate_days_till_full(int(config['EMAIL']['SD_size']))

    #check to see of the plc storage will fill up with the given days 
    if days_left <= warning_days and days_left > 0:
        days_rem.append((address, days_left))
    elif days_left is 0:
        full_plcs.append(address)


    #download files to the local pc storage
    new_files = sps.download_files_to_pc(plc_dest, datetime.datetime.now())

    #upload new files to Host Point
    HostpointClient.upload_to_Hostpoint(config['HOSTPOINT']['hostname'], config['HOSTPOINT']['username'], config['HOSTPOINT']['password'], plc_dest, new_files)

    #disconnect from the plc
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




    # print("Downloading Files From SPS...")
    # print("Uploading Files To HostPoint...")  
    # print("Done!")
    # print ('print tuple: ' + str(tupleresult))
    # print ('Total Usage In MB: ' + str(totalusageMB) + 'MB')
    # print ('Avarage file size per day in MB: ' + str(avg_size) + 'MB')
    # print ('Size left before full: ' + str(size_left) + 'MB')
    # print ('Days left before storage is full: ' + str(days_left) + ' days')
    # print (failed_connections)
    # print (days_rem)
    # print (full_plcs)
