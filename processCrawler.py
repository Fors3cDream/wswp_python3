import time
import urllib.parse
import threading
import multiprocessing
from mongoCache import MongoCache
from mongoQueue import MongoQueue
from downloader import Downloader

SLEEP_TIME = 1

def threadedCrawler(seedUrl, delay=5, cache=None, scrapeCallbak=None, userAgent='wswp', proxies=None, numRetries=1, maxThreads=10,timeout=60):
    """
    crawl using multiple processing
    """

    crawlQueue = MongoQueue()
    crawlQueue.clear()
    crawlQueue.push(seedUrl)

    downloader = Downloader(cache=cache, delay=delay, userAgent=userAgent, proxies=proxies, numRetries=numRetries, timeout=timeout)

    def processQueue():
        while True:
            # keep track that are processing url
            try:
                url = crawlQueue.pop()
            except KeyError:
                # Currently no urls to process
                break
            else:
                html = downloader(url)
                if scrapeCallbak:
                    try:
                        links = scrapeCallbak(url, html) or []
                    except Exception as e:
                        print('Error in callback for: {}:{}'.format(url, e))
                    else:
                        for link in links:
                            # add this new link to queue
                            crawlQueue.push(normalize(seedUrl, link))
                crawlQueue.complete(url)

        # wait for all download threads to finish
        threads = []
        while threads or crawlQueue:
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < maxThreads and crawlQueue.peek():
                # can start some more threads
                thread = threading.Thread(target=processQueue)
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)
            time.sleep(SLEEP_TIME)

def processCrawler(args, **kwargs):
    numCpus = multiprocessing.cpu_count()
    print('Starting {} processes'.format(numCpus))
    processes = []
    for i in range(numCpus):
        p = multiprocessing.Process(target=threadedCrawler,args=[args], kwargs=kwargs)
        p.start()
        processes.append(p)
    # wait for prcesses to complete
    for p in processes:
        p.join()

def normalize(seedUrl, link):
    link, _ = urllib.parse.urldefrag(link)
    return urllib.parse.urljoin(seedUrl, link)
