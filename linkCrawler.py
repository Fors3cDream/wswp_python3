import re
import urllib.parse

import Queue
from downloadWithProxy import download

from wswp_1.Throttle import Throttle
from wswp_1.getRobots import getRobots


def linkCrawler(seed_url, link_regex=None, max_depth=-1, delay=5, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=3):
    crawl_queue = Queue.deque([seed_url])
	# 通过set类型进行去重处理
	#seen = set(crawl_queue)
    seen = {seed_url:0}
    # 记录有多少链接需要下载
    num_urls = 0
    rp = getRobots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

	while crawl_queue:
		url = crawl_queue.pop()

		# 检查url是否可以被采集
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links = []

            depth = seen[url]
            if depth != max_depth:
                if link_regex:
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)

                    if link not in seen:
                        seen[link] = depth + 1
                        if sameDomain(seed_url, link):
                            crawl_queue.append(link)
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print('Blocked by robots.txt:', url)

def linkCrawler_v2(seed_url, link_regex):
	crawl_queue = [seed_url]
	# 通过set类型进行去重处理
	seen = set(crawl_queue)
	while crawl_queue:
		url = crawl_queue.pop()
		html = download(url)
		for link in get_links(html):
			if re.match(link_regex, link):
				link = urllib.parse.urljoin(seed_url, link)
				if link not in seen:
					seen.add(link)
					crawl_queue.add(link)

def linkCrawler_v1(seed_url, link_regex):
    """
    Crawl from the given seed_url following links matched by link_regex
    :param seed_url:
    :param link_regex:
    :return:
    """
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)

        # filter for links matching our regular expression
        for link in get_links(html):
            if re.match(link_regex, link):
                crawl_queue.append(link)

def get_links(html):
    """
    Return a list of links from html
    :param html:
    :return:
    """

    webpage_regex = re.compile('<a\shref="(.*?)"', re.IGNORECASE)

    # list of all links from the webpage
    return webpage_regex.findall(str(html))

def normalize(seed_url, link):
    link, _ = urllib.parse.urldefrag(link) # remove hash to avoid duplicates
    return urllib.parse.urlparse(seed_url, link)

def sameDomain(link1, link2):
    return urllib.parse.urlparse(link1).netloc == urllib.parse.urlparse(link2).netloc