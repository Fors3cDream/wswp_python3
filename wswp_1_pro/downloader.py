import urllib.request
import urllib.parse
import urllib.error


def download(url, headers, proxy, numRetries, data=None):
    print("正在下载:", url)
    request = urllib.request.Request(url, data, headers)
    opener = urllib.request.build_opener()
    if proxy:
        proxyParams = { urllib.parse.urlparse(url).scheme: proxy }
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
            if numRetries > 0 and 500<=code<600:
                return download(url, headers, proxy, numRetries - 1, data)
        else:
            code = None
    return html