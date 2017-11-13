import sys
from threadCrawler import threadCrawler
from diskCache import DiskCache
from alexaCb import AlexaCallback

def main(maxThreads):
    scrapeCallback = AlexaCallback()
    cache = DiskCache()
    threadCrawler(scrapeCallback.seedUrl, scrapeCallback=scrapeCallback, cache=cache, maxThreads=maxThreads, timeout=10)

if __name__ == '__main__':
    maxThreads = int(sys.argv[1])
    main(maxThreads)