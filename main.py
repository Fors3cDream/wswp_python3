from wswp_1_pro.linkCrawler import linkCrawler

if __name__ == "__main__":

    # url = 'http://www.freebuf.com/articles/rookie/151327.html'
    #
    # url_500 = 'http://httpstat.us/500'
    #
    # html = download_v2(url)
    #
    # print(html)
    # linkCrawler('http://example.webscraping.com', '.*?/(index|view)')
    linkCrawler('http://example.webscraping.com', '.*?/(index|view).*?', delay=3,numRetries=3,userAgent='BadCrawler')
    #linkCrawler('http://example.webscraping.com', '.*?/(index/view)', delay=3, numRetries=3, maxDepth=1,userAgent='GoodCrawler')
