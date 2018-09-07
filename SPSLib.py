import os

class SPSLib:

    def __init__(self, client, default_destination=""):
        self.client = client
        self.default_destination = default_destination

    def change_to_date(self, date):
        year = str(date.year)
        month = str(date.month).zfill(2)
        self.client.cwd('/' + year + '/' + month)

    def download_files_for_month(self, date):
        directory = self.client.pwd()
        self.change_to_date(date)
        files = self.ls()
        for file in files:
            outfile = open(self.default_destination + file, 'wb')
            self.client.retrbinary("retr " + file, outfile.write)
            outfile.close()
        self.client.cwd(directory)

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

    def ls(self):
        return self.client.nlst()

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

    def close_connection(self):
        self.client.quit()

    @staticmethod
    def clean_directory(directory):
        for file in os.listdir(directory):
            if '.xls' in file or '.xlsx' in file:
                os.unlink(os.path.join(directory, file))
