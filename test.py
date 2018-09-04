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

# message = EMail(config['EMAIL']['username'], config['EMAIL']['recipient'])
# message.set_subject("Test Email Send From Library")
# message.set_body("The current SPS with the address of: 111111 has used up " + str(totalusageMB) + " MB.")

# sender = EMailSender(config['EMAIL']['smtp_server'], config['EMAIL']['smtp_port'])
# sender.login(config['EMAIL']['username'],config['EMAIL']['password'])
# sender.send_message(message)
# sender.quit()

