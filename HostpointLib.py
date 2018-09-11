from ftplib import FTP
import os


class HostpointClient:
    def __init__(self, hostname, username, password):
        """The Constructor
        
        Arguments:
            hostname {string} -- hostname of the HostPoint ftp server
            username {string} -- username for the HostPoint ftp server
            password {string} -- password for said user
        """

        self.client = FTP(hostname)
        self.client.login(username, password)

    def upload_file(self, filename):
        """Upload a single file from the local storage to the FTP server
        
        Arguments:
            filename {string} -- Path to the file on the local storage to upload
        """

        file = open(filename, 'rb')
        self.client.storbinary('STOR %s' % os.path.basename(filename), file)
        file.close()

    def upload_files(self, filelist):
        """Upload a list of files from the local storage to the FTP server
        
        Arguments:
            filelist {list[string]} -- A list of paths to files on the local storage
        """

        for file in filelist:
            self.upload_file(file)

    def upload_all_files_in_directory(self, directory):
        """Upload all the files in a given directory on the local storage to the FTP server
        
        Arguments:
            directory {string} -- Path to the directory on the local storage
        """

        self.upload_files([os.path.join(directory, file) for file in os.listdir(directory)])


    def close(self):
        """Close the connection with HostPoint server
        """

        self.client.close()