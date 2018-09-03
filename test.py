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





config = configparser.ConfigParser()
config.read('collection.conf')

addresses = (config['DEFAULT']['addresses']).split(',')
user = config['DEFAULT']['username']
password = config['DEFAULT']['password']
destination = config['DEFAULT']['default_destination']

ftp = FTP('10.0.0.99')
ftp.login(user=user, passwd=password)

sps = SPSLib(ftp)
totalusage = sps.get_total_size('/')
totalusageMB = round(totalusage/(1024*1024), 2) 
print ('Total Usage In MB: ' + str(totalusageMB) + 'MB')

sps.close_connection()

message = EMail(config['EMAIL']['username'], config['EMAIL']['recipient'])
message.set_subject("Test Email Send From Library")
message.set_body("The current SPS with the address of: 111111 has used up " + str(totalusageMB) + " MB.")

sender = EMailSender(config['EMAIL']['smtp_server'], config['EMAIL']['smtp_port'])
sender.login(config['EMAIL']['username'],config['EMAIL']['password'])
sender.send_message(message)
sender.quit()

