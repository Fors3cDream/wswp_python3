import re
import urllib.parse
import urllib.robotparser
from collections import deque
from .Throttle import Throttle
from .downloader import download

def getRobots(url):
    """
    Initial robots parser for this domain
    :param url:
    :return:
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp

def normalize(seedUrl, link):
    """
    Normalize this URL by removing hash and adding domain
    :param seedUrl:
    :param link:
    :return:
    """
    link, _ = urllib.parse.urldefrag(link) # remove hash to avoid duplicates
    return urllib.parse.urljoin(seedUrl, link)

def sameDomain(url1, url2):
    """
    Return True if both URL's belong to same domain
    :param url1:
    :param url2:
    :return:
    """
    return urllib.parse.urlparse(url1).netloc == urllib.parse.urlparse(url2).netloc

def getLinks(html):
    """
    Return a list of links from html
    :param html:
    :return:
    """
    webpageRegex = re.compile('<a\shref="(.*?)"',re.IGNORECASE)
    return webpageRegex.findall(str(html))

def linkCrawler(seedUrl, linkRegex=None, delay=5, maxDepth=-1, maxUrls=-1, headers=None, userAgent='wswp', proxy=None, numRetries=1, scrapeCallBack=None):
    """
    Crawl from the given seed URL following links matched by linkRegex
    :param seedUrl:  起始url
    :param linkRegx: 链接匹配的正则表达式
    :param delay: 延迟时间
    :param maxDepth: 最深的层次
    :param maxUrls:  最多的url数量
    :param headers: http请求头
    :param userAgent: http头中的userAgent选项
    :param proxy: 代理地址
    :param numRetries: 重新下载次数
    :return:
    """
    crawlQueue = deque([seedUrl])
    seen = { seedUrl:0}
    numUrls = 0
    rp = getRobots(seedUrl)
    throttle = Throttle(delay)

    headers = headers or {}
    if userAgent:
        headers['User-agent'] = userAgent

    while crawlQueue:
        url = crawlQueue.pop()

        if rp.can_fetch(userAgent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, numRetries=numRetries)
            links = []

            if scrapeCallBack:
                links.extend(scrapeCallBack(url, html) or [])

            depth = seen[url]
            if depth != maxDepth:
                if linkRegex:
                    links.extend(link for link in getLinks(html) if re.match(linkRegex, link))

                for link in links:
                    link = normalize(seedUrl, link)

                    if link not in seen:
                        seen[link] = depth + 1

                        if sameDomain(seedUrl, link):
                            crawlQueue.append(link)

            numUrls += 1
            if numUrls == maxUrls:
                break

        else:
            print('Blocked by robots.txt',url)

