import urllib.parse
import datetime
import time

class Throttle:
    """
    对一个域名访问时在前后两次访问之间添加一个延时。
    """
    def __init__(self, delay):
        self.delay = delay
        # 同一个域名的上一次访问时间
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc

        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds

            if sleep_secs > 0:
                # 域名刚被访问过，需要延时
                time.sleep(sleep_secs)

        # 更新上次访问时间
        self.domains[domain] = datetime.datetime.now()