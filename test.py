from ftplib import FTP
import sys
import os
import datetime
import configparser
from SPSLib import SPSLib

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
totalusageMB = totalusage/(1024*1024) 
print ('Total Usage In MB: ' + str(totalusageMB) + 'MB')

sps.close_connection()

