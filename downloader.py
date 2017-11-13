import urllib.request
import urllib.parse
import urllib.error
from Throttle import Throttle
import socket
import random

DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60


class Downloader:
    def __init__(self,delay=DEFAULT_DELAY,userAgent=DEFAULT_AGENT,proxies=None,numRetries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT, opener=None,cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.userAgent = userAgent
        self.proxies = proxies
        self.numRetries = numRetries
        self.cache = cache
        self.opener = None

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not available in cache
                pass
            else:
                if self.numRetries >0 and 500<=result['code']<600:
                    # server error so ignore result from cache and re-download
                    result = None

        if result is None:
            # result was not loaded from cache so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.userAgent}
            result = self.download(url, headers, proxy=proxy,numRetries=self.numRetries)
            if self.cache:
                # save result to cache
                    self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, numRetries, data=None):
        print("正在下载:", url)
        request = urllib.request.Request(url, data, headers)
        opener = self.opener or urllib.request.build_opener()
        if proxy:
            proxyParams = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxyParams))

        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except urllib.error.URLError as e:
            print('下载错误:', e.reason)
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if numRetries > 0 and 500 <= code < 600:
                    return self.download(url, headers, proxy, numRetries - 1, data)
            else:
                code = None
        return {'html':html,'code':code}

