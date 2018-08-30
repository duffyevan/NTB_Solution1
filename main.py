from ftplib import FTP
import sys
import os
import datetime
import configparser
from SPSLib import SPSLib

def collect_data():
    config = configparser.ConfigParser()
    config.read('collection.conf')

    addresses = (config['DEFAULT']['addresses']).split(',')
    user = config['DEFAULT']['username']
    password = config['DEFAULT']['password']
    destination = config['DEFAULT']['default_destination']

    if not os.path.isdir(destination): # Make sure the destination dir exists
        os.makedirs(destination) # Create it if needed

    for address in addresses:
        try:
            # Create Client and Log In
            ftp = FTP(address)
            ftp.login(user=user, passwd=password)
            sps = SPSLib(ftp, default_destination=destination)
            sps.download_files_for_month(datetime.datetime.now())
            ftp.quit()

        except:
            print("Error Retrieving Data From SPS at address: " + address)
            print("--> ", sys.exc_info()[0])