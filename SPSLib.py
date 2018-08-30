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

    def get_total_size(self, directory):
        return_dir = self.client.pwd()
        size = 0
        for filename in self.client.nlst(directory):
            self.client.cwd(return_dir)
            try:
                self.client.cwd(filename)
                size += self.get_total_size('./')
            except:
                self.client.voidcmd('TYPE I')
                size += self.client.size(filename)
        return size

    def close_connection(self):
        self.client.quit()