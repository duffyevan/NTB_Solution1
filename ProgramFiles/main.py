import configparser

import datetime
import logging
import os

from EMailLib import EMail, EMailSender
from HostpointLib import HostpointClient
from SPSLib import SPSLib, SPSConnectionException

# setup reading the config file
config = configparser.ConfigParser()
config.read('../User/collection.conf')

# set the veriables according to the config file
addresses = (config['DEFAULT']['addresses']).split(',')
user = config['DEFAULT']['username']
password = config['DEFAULT']['password']
destination = config['DEFAULT']['default_destination'].replace("~", "c:\\Users\\" + os.getlogin())
numretries = int(config['DEFAULT']['number_connection_retries'])
retrydelay = int(config['DEFAULT']['connection_retry_delay'])
warning_days = int(config['EMAIL']['warning_days'])
log_file = config['DEFAULT']['log_file_location']

logging.basicConfig(filename=config['DEFAULT']['log_path'], level=logging.INFO,
                    format='%(asctime)s: %(levelname)s : %(message)s')

# list veriables that will be used for email perposes
failed_connections = []
days_rem = []
full_plcs = []

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s: %(levelname)s : %(message)s')
logging.info("Starting")

# check to see of a download folder exists for the given path on the pc
SPSLib.path_exist(destination)

# For each plc address, do the following
for address in addresses:

    #Check to see if a folder exists for the given plc address on the local pc
    plc_dest = (destination + address + '\\')
    SPSLib.path_exist(plc_dest)

    logging.info("Attempting to log into SPS at " + address)

    #log in to the plc via ftp
    try:
        sps = SPSLib(address, user, password, default_destination=plc_dest, numretries=numretries,
                     retrydelay=retrydelay)
    except SPSConnectionException as ex:
        failed_connections.append(address)
        logging.error("Failed to log into SPS at " + address)
        continue

    logging.info("Successfully logged into SPS at " + address)

    # finds days left before sps is full
    days_left = sps.calulate_days_till_full(int(config['EMAIL']['SD_size']))
    logging.info("SPS at " + address + " has " + days_left + " days till threshold data used")

    # check to see of the plc storage will fill up with the given days
    if days_left <= warning_days and days_left > 0:
        days_rem.append((address, days_left))
        logging.warning("SPS at " + address + " is nearly full!")
    elif days_left <= 0:
        full_plcs.append(address)
        logging.error("SPS at " + address + " is full!")

    logging.info("Beginning file download from SPS at " + address)
    #download files to the local pc storage
    new_files = sps.download_files_to_pc(plc_dest, datetime.datetime.now())

    logging.info("Beginning file upload to HostPoint from SPS at " + address)
    #upload new files to Host Point
    HostpointClient.upload_to_Hostpoint(config['HOSTPOINT']['hostname'], config['HOSTPOINT']['username'], config['HOSTPOINT']['password'], plc_dest, new_files)

    logging.info("Disconnecting from SPS at " + address)
    #disconnect from the plc
    sps.close_connection()

# parse the email recipient text file
names, emails = EMail.get_contacts('email_templates/email_addresses.txt')

logging.info("Opening SMTP connection")
#log into the email
sender = EMailSender.setup_email_sender(config['EMAIL']['smtp_server'], config['EMAIL']['smtp_port'], config['EMAIL']['username'], config['EMAIL']['password'])


# send the emails
if len(failed_connections) > 0:
    logging.warning("Sending warning emails about failed connections")
    sender.send_email(config['EMAIL']['username'], zip(names, emails), 'email_templates/ConnectionError.temp', "SPS Connection Error", failed_connections)

if len(full_plcs) > 0:
    logging.warning("Sending warning emails about full SPSs")
    sender.send_email(config['EMAIL']['username'], zip(names, emails), 'email_templates/SPS_FullWarning.temp', "SPSs Are Full", full_plcs)

if len(days_rem) > 0:
    logging.warning("Sending warning emails about almost full SPSs")
    sender.send_email_almost_full(config['EMAIL']['username'], zip(names, emails), 'email_templates/DaysLeftWarning.temp', "SPSs Are Almost Full", days_rem, config['EMAIL']['warning_days'])


logging.info("Closing SMTP connection")
# Terminate the SMTP session and close the connection
sender.quit()

logging.info("Done! Exiting")
