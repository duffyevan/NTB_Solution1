class SPSLib:

    def __init__(self, client):
        self.client = client

    def change_to_date(self, date):
        year = str(date.year)
        month = str(date.month).zfill(2)
        self.client.cwd('/' + year + '/' + month)

    def download_files_for_month(self, date):
        directory = self.client.pwd()
        self.change_to_date(date)
        files = self.ls()
        for file in files:
            outfile = open(file, 'wb')
            self.client.retrbinary("retr " + file, outfile.write)
            outfile.close()
        self.client.cwd(directory)

    def ls(self):
        return self.client.nlst()