import urllib.request
import urllib.error
import urllib.parse
from urllib.request import urlopen

def download(url, headers, proxy, num_retries, data=None):
    print("Downloading:", url)

    request = urllib.request.Request(url,data,headers)

    opener = urllib.request.build_opener()

    if proxy:
        proxy_params = { urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))

    try:
        #html = urlopen(request).read()
        response = opener.open(request)
        html = response.read()
        code = response.code

    except urllib.error.URLError as e:
        print("Download Error:", e.reason)

        html = None

        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500<=code<600:
                download(url,headers, proxy, num_retries - 1, data)
        else:
            code = None

    return html