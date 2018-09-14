from ftplib import FTP
import os


class HostpointClient:
    ## The Constructor
    # @param hostname {string} hostname of the HostPoint ftp server
    # @param username {string} username for the HostPoint ftp server
    # @param password {string} password for said user

    def __init__(self, hostname, username, password):
        self.client = FTP(hostname)
        self.client.login(username, password)

    ## Upload a single file from the local storage to the FTP server
    # @param filename {string} Path to the file on the local storage to upload

    def upload_file(self, filename):
        file = open(filename, 'rb')
        self.client.storbinary('STOR %s' % os.path.basename(filename), file)
        file.close()

    ## Upload a list of files from the local storage to the FTP server
    # @param filelist {list[string]} A list of paths to files on the local storage

    def upload_files(self, filelist):
        for file in filelist:
            self.upload_file(file)

    ## Upload all the files in a given directory on the local storage to the FTP server
    # @param directory {string} Path to the directory on the local storage

    def upload_all_files_in_directory(self, directory):
        self.upload_files([os.path.join(directory, file) for file in os.listdir(directory)])


    ## Close the connection with HostPoint server
    def close(self):
        self.client.close()


    #####Milap Changes
    ##

    ## Logs into Host Point and uploads new files to it.
    # @param hostname {string} Name name of the host (Their login address)
    # @param username {string} Username used for login
    # @param password {string} Password used for login
    # @param localDest {string} the download path on the local pc
    # @param newFiles {list[string]} List of names of the new files that need to be uploaded
    @staticmethod
    def upload_to_Hostpoint(hostname, username, password, localDest, newFiles):
        hp = HostpointClient(hostname , username, password)
        hp.upload_files([os.path.join(localDest, file) for file in newFiles]) 