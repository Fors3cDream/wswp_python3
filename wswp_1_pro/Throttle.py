import time
import datetime
import urllib.parse

class Throttle:
    """
    Throttle downloading by sleeping between requests to same domain
    """

    def __init__(self, delay):
        # Amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domain = {}

    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc
        lastAccessed = self.domain.get(domain)

        if self.delay > 0 and lastAccessed is not None:
            sleepSec = self.delay - (datetime.datetime.now() - lastAccessed).seconds
            if sleepSec > 0:
                time.sleep(sleepSec)
        self.domain[domain] = datetime.datetime.now()