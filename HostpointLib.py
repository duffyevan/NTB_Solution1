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
