from urllib.request import urlopen
import urllib.error

def download_v1(url):

    return urlopen(url).read()

def download_v2(url):

    print("正在下载: ", url)

    try:
        html = urlopen(url).read()

    except urllib.error.URLError as e:
        print('下载错误:', e.reason)
        html = None

    return html

def download(url, num_retries=2):
    print("正在下载:", url)

    try:
        html = urlopen(url).read()
    except urllib.error.URLError as e:
        print('下载错误:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx http errors
                return download(url, num_retries - 1)

    return html