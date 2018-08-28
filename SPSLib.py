def change_to_date(client, date):
    year = str(date.year)
    month = str(date.month).zfill(2)
    client.cwd('/' + year + '/' + month)