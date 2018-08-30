from ftplib import FTP
import sys
import os
import datetime
import getpass
import configparser
import smtplib
from SPSLib import SPSLib

config = configparser.ConfigParser()
config.read('collection.conf')

addresses = (config['DEFAULT']['addresses']).split(',')
user = config['DEFAULT']['username']
password = config['DEFAULT']['password']
destination = config['DEFAULT']['default_destination']

# s = smtplib.SMTP(config['EMAIL']['smtp_server'] + ':' + config['EMAIL']['smtp_port'])
# s.ehlo()
# s.starttls()
# s.login(config['EMAIL']['username'],getpass.getpass('Enter Email Password: '))


# gmailuser =  'evanlduffy@gmail.com'
# gmailpass = getpass.getpass()

# try:
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.ehlo()
#     server.login(gmailuser, gmailpass)

# except:
#     print ('something went wrong', sys.exc_info()[0])



ftp = FTP('10.0.0.99')
ftp.login(user=user, passwd=password)

sps = SPSLib(ftp)
totalusage = sps.get_total_size('/')
totalusageMB = totalusage/(1024*1024) 
print ('Total Usage In MB: ' + str(totalusageMB) + 'MB')



sps.close_connection()

