import csv
from zipfile import ZipFile
from io import StringIO
from mongoCache import MongoCache

class AlexaCallback:
    def __init__(self, maxUrls=1000):
        self.maxUrls = maxUrls
        self.seedUrl = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == self.seedUrl:
            urls = []
            cache = MongoCache()
            with ZipFile(StringIO(html)) as zf:
                csvFilename = zf.namelist()[0]
                for _, website in csv.reader(zf.open(csvFilename)):
                    if 'http://' + website not in cache:
                        urls.append('http://' + website)
                        if (len(urls) == self.maxUrls):
                            break
            return urls