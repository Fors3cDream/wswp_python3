import os
import re
import urllib.parse
import shutil
import zlib
import hashlib
from datetime import datetime, timedelta

try:
    import cPickle as pickle
except ImportError:
    import pickle

class DiskCache:

    def __init__(self, cacheDir='cache', expires=timedelta(days=30),compress=True):
        """
        :param cacheDir: 缓存存放目录
        :param expires: 缓存过期时间
        :param compress: 是否压缩
        """
        self.cacheDir = cacheDir
        self.expires = expires
        self.compress = compress

    def __getitem__(self,url):
        """
        Load data from disk for this URL
        :param url:
        :return:
        """
        path = self.urlToPath(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                if self.hasExpired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            # url has not yet been cached
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """
        Save data to disk for this url
        :param url:
        :param result:
        :return:
        """
        path = self.urlToPath(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dumps((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __delitem__(self, url):
        """
        Remove the value at this key and any empty parent sub-directories
        :param url:
        :return:
        """
        path = self._keyPath(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    def urlToPath(self, url):
        """
        Create file system path for this url
        :param url:
        :return:
        """
        components = urllib.parse.urlparse(url)

        # when empty path set to /index.html
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'

        filename = components.netloc + path + components.query

        # Replace invalid characters
        filename = re.sub('[^/0-9A-Za-z\-.,;_]','_', filename)

        # restrict maxinum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))

        return os.path.join(self.cacheDir, filename)

    def hasExpired(self, timestamp):
        """
        Return whether this timestamp has expired
        :param timestamp:
        :return:
        """
        return datetime.utcnow() > timestamp + self.expires

    def clear(self):
        """
        Remove all the cached values
        :return:
        """
        if os.path.exists(self.cacheDir):
            shutil.rmtree(self.cacheDir)