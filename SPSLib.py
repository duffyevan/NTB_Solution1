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

    def ls(self):
        return self.client.nlst()

    def get_total_size(self):
        size = 0
        for filename in self.client.nlst('/'):
            # print (filename)
            for filename2 in self.client.nlst('/' + filename):
                # print ('--> ' + filename2)                
                for filename3 in self.client.nlst('/' + filename + '/' + filename2):
                    # print ('------> ' + filename3)                                
                    size += self.client.size('/' + filename + '/' + filename2 + '/' + filename3)
        return size

    def close_connection(self):
        self.client.quit()