import re
import lxml.html
from wswp_1_pro.linkCrawler import linkCrawler

FIELDS = ['area', 'population', 'iso', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours']

def scrapeCallBack(url, html):
    if re.search('/view/', url):
        tree = lxml.html.fromstring(str(html))
        row = [tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % field)[0].text_content() for field in FIELDS]
        for text, content in zip(FIELDS,row):
            print(text + ' : ' + content)

if __name__ == "__main__":
    linkCrawler('http://example.webscraping.com/', '.*?/(index|view)', maxDepth=2, scrapeCallBack=scrapeCallBack)