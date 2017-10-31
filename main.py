from linkCrawler import linkCrawler
from diskCache import DiskCache

if __name__ == '__main__':
    linkCrawler('http://example.webscraping.com/', '.*?/(index|view)', cache=DiskCache())