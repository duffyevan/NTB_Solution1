import os
from ftplib import FTP
import time

class SPSConnectionException(Exception):
    def __init__(self):
        pass

class SPSLib:

    ## The Constructor
    # @param client {FTP} An FTP client to be used as the connection
    # @param default_destination {string} Path to where the files are automatically downloaded 
    # @return default_destination {string} Default download destination on the local storage. Defaults to the current working directory (default: {""} )
    def __init__(self, address, username, password, default_destination="", numretries=1, retrydelay=1):
        self.client = SPSLib._create_ftp_client(address, username, password, numretries, retrydelay)
        self.default_destination = default_destination
    
    @staticmethod
    def _create_ftp_client(address, username, password, numretries, retrydelay):
        success = False
        ftp = None
        for n in range(0, numretries):
            try:
                ftp = FTP(address)
                ftp.login(user=username, passwd=password)
                success = True
            except:
                print('Connection Attempt ' + str(n+1) + ' to ' + address + ' Failed')
                time.sleep(retrydelay)

        if not success:
            print('Error Connecting To PLC at ' + address)
            raise SPSConnectionException()
        return ftp    

    ## Change directory to the directory corresponding to the month of the date
    # @param date {datetime} The date to get the month from and change to the corresponding folder
    def change_to_date(self, date):
        year = str(date.year)
        month = str(date.month).zfill(2)
        self.client.cwd('/' + year + '/' + month)

    ## Download all files for a given month by the date
    # @param date {datetime} The date to get the month from to then download all files for that month
    def download_files_for_month(self, date):
        directory = self.client.pwd()
        self.change_to_date(date)
        files = self.ls()
        for file in files:
            outfile = open(self.default_destination + file, 'wb')
            self.client.retrbinary("retr " + file, outfile.write)
            outfile.close()
        self.client.cwd(directory)

    ## Download all files for a given day by the date
    # @param date {datetime} The date to download all the files from that day
    def download_files_for_day(self, date):
        directory = self.client.pwd()
        self.change_to_date(date)
        datestring = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
        files = self.ls()
        num_files = 0
        for file in files:
            if datestring in file:
                num_files = num_files+1
                outfile = open(self.default_destination + file, 'wb')
                self.client.retrbinary("retr " + file, outfile.write)
                outfile.close()
        self.client.cwd(directory)
        if num_files is 0:
            raise Exception('No Files Available For Date ' + datestring)

    ## List the contents of the current directory on the PLC
    # @param list[string] a list of file names corresponding to the files in the current working directory 
    def ls(self):
        return self.client.nlst()

    ## Get the total disk usage of the files accessible to the FTP client
    # @param directory {string} Path to the directory on the PLC
    # @return int The number of bytes used by all the files accessible to the FTP server
    def get_total_size(self, directory):
        return_dir = self.client.pwd()
        size = 0
        files = 0

        for filename in self.client.nlst(directory):
            self.client.cwd(return_dir)
            try:
                self.client.cwd(filename)
                tupleresult =  self.get_total_size('./')
                size += tupleresult[0]
                files += tupleresult[1]
            except:
                self.client.voidcmd('TYPE I')
                size += self.client.size(filename)
                files += 1
        return (size, files)

    ## Close the connection to the SPS
    def close_connection(self):
        self.client.quit()


    ## Delete all files in the given directory on the local storage (for use when organizing downloaded files)
    # @param directory {string} Path to the directory on the local storage to delete all files from
    @staticmethod
    def clean_directory(directory):
        for file in os.listdir(directory):
            if '.xls' in file or '.xlsx' in file:
                os.unlink(os.path.join(directory, file))





####Milap changes##

    ## Calculates the number of days left before the PLC storage is expected to be full.
    # @param SD_size {intiger} Size of the storage on the PLC in MB
    # @return days_left Days left before PLC is full
    def calulate_days_till_full(self, SD_size):
        tupleresult = self.get_total_size('/')
        totalusage = tupleresult[0]
        totalusageMB = round(totalusage/(1024*1024), 2) 
        avg_size = round(totalusageMB/tupleresult[1], 2)
        size_left = round((SD_size - totalusageMB), 2)
        days_left = int(size_left/avg_size)
        return days_left


    ## Checks to see of the given path is valid on the local PC storage. If it is not, then it creates the path and folders.
    # @param destination {string} Path to the directory on the local storage
    @staticmethod
    def path_exist(destination):
        if not os.path.exists(destination):
            os.makedirs(destination)


    ## Downloads all the files for a given month form the sps into the local directory on the pc.
    # @param destination {string} Path to the directory on the local storage
    # @param datetime {string} Date of the month that will be downloaded
    # @return new_files List of new files
    def download_files_to_pc(self, destination, datetime):
        files_before_download = os.listdir(destination) 
        self.download_files_for_month(datetime) 
        files_after_download = os.listdir(destination) 
        new_files = list(set(files_after_download) - set(files_before_download)) 
        return new_files
