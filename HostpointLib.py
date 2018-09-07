from ftplib import FTP
import os

class HostpointClient:
    def __init__(self, hostname, username, password):
        self.client = FTP(hostname)
        self.client.login(username, password)

    def upload_file(self, filename):
        file = open(filename, 'rb')
        self.client.storbinary('STOR %s' % os.path.basename(filename), file)
        file.close()

    def upload_files(self, filelist):
        for file in filelist:
            self.upload_file(file)

    def upload_all_files_in_directory(self, directory):
        self.upload_files([os.path.join(directory, file) for file in os.listdir(directory)])


    def close(self):
        self.client.close()