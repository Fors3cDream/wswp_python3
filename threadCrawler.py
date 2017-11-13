import time
import threading
import urllib.parse
from downloader import Downloader

SLEEP_TIME = 3

def threadCrawler(seedUrl, delay=5, cache=None, scrapeCallback=None, userAgent='wswp', proxies=None, numRetries=1, maxThreads=10, timeout=60):
    """
    Crawl this website in multiple threads
    """
    crawlQueue = [seedUrl]
    # The url's that have been seen
    seen = set([seedUrl])
    downloader = Downloader(cache=cache, delay=delay, userAgent=userAgent, proxies=proxies, numRetries=numRetries, timeout=timeout)

    def processQueue():
        while True:
            try:
                url = crawlQueue.pop()
            except IndexError:
                break
            else:
                html = downloader(url)
                if scrapeCallback:
                    try:
                        links = scrapeCallback(url, html) or []
                    except Exception as e:
                        print('Error in callback for: {}:{}'.format(url, e))
                    else:
                        for link in links:
                            link = normalize(seedUrl, link)
                            if link not in seen:
                                seen.add(link)
                                crawlQueue.append(link)

    # wait for all download threads to finish
    threads = []
    while threads or crawlQueue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)

        while len(threads) < maxThreads and crawlQueue:
            # can start some more threads
            thread = threading.Thread(target=processQueue)
            thread.setDaemon(True) # set daemon so main thread can exit when receives ctrl-c
            thread.start()
            threads.append(thread)

        # all threads have been processed
        # sleep temporarily so CPU an focus execution on other threads
        time.sleep(SLEEP_TIME)

    def normalize(seedUrl, link):
        """
        Normalize this url by removing hash and adding domain
        :param seedUrl:
        :param link:
        :return:
        """

        link, _ = urllib.parse.urlfrag(link)
        return urllib.parse.urljon(seedUrl, link)