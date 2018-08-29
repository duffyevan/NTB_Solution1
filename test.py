from ftplib import FTP
import sys
import datetime
import configparser
from data_collection_automation.SPSLib import *

config = configparser.ConfigParser()
config.read('collection.conf')

addresses = (config['DEFAULT']['addresses']).split(',')
user = config['DEFAULT']['username']
password = config['DEFAULT']['password']
destination = config['DEFAULT']['default_destination']

for address in addresses:
    try:
        # Create Client and Log In
        ftp = FTP(address)
        ftp.login(user=user, passwd=password)
        sps = SPSLib(ftp)
        sps.download_files_for_month(datetime.datetime.now())
        ftp.quit()

    except:
        print("Error Retrieving Data From SPS at address: " + address)


