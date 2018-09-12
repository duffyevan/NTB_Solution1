import os

class SPSLib:

    ## The Constructor
    # @param client {FTP} An FTP client to be used as the connection
    # @param default_destination {string} Path to where the files are automatically downloaded 
    # @return default_destination {string} Default download destination on the local storage. Defaults to the current working directory (default: {""})
    def __init__(self, client, default_destination=""):
            
        self.client = client
        self.default_destination = default_destination
    
    ## Change directory to the directory corresponding to the month of the date
    # @param date {datetime}The date to get the month from and change to the corresponding folder
    def change_to_date(self, date):
        year = str(date.year)
        month = str(date.month).zfill(2)
        self.client.cwd('/' + year + '/' + month)

    ## Download all files for a given month by the date
    # @param date {datetime}The date to get the month from to then download all files for that month
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
    # @param date {datetime}The date to download all the files from that day
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
    # @param list[string]a list of file names corresponding to the files in the current working directory 
    def ls(self):
        return self.client.nlst()

    ## Get the total disk usage of the files accessible to the FTP client
    # @param directory {string}Path to the directory on the PLC
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
    # @param directory {string}Path to the directory on the local storage to delete all files from
    @staticmethod
    def clean_directory(directory):
        for file in os.listdir(directory):
            if '.xls' in file or '.xlsx' in file:
                os.unlink(os.path.join(directory, file))
