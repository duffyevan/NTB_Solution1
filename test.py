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
        sps = SPSLib(address, user, password, default_destination=plc_dest, numretries=numretries, retrydelay=retrydelay)
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


#parse the email recipient text file
names, emails = EMail.get_contacts('email_templates/email_addresses.txt')

#log into the email
sender = EMailSender.setup_email_sender(config['EMAIL']['smtp_server'], config['EMAIL']['smtp_port'], config['EMAIL']['username'], config['EMAIL']['password'])

#send the emails
if len(failed_connections) > 0:
    sender.send_email(config['EMAIL']['username'], zip(names, emails), 'email_templates/ConnectionError.temp', "SPS Connection Error", failed_connections)

if len(full_plcs) > 0:
    sender.send_email(config['EMAIL']['username'], zip(names, emails), 'email_templates/SPS_FullWarning.temp', "SPSs Are Full", full_plcs)

if len(days_rem) > 0:
    sender.send_email_almost_full(config['EMAIL']['username'], zip(names, emails), 'email_templates/DaysLeftWarning.temp', "SPSs Are Almost Full", days_rem, config['EMAIL']['warning_days'])

# Terminate the SMTP session and close the connection
sender.quit()
