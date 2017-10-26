from bs4 import BeautifulSoup
from wswp_1_pro.downloader import download


url = 'http://example.webscraping.com/places/default/view/China-47'

html = download(url, headers={'User-agent':'wswp'}, proxy=None, numRetries=2)

soup = BeautifulSoup(html, "html.parser")

# 先定位面积的父标签
tr = soup.find(attrs={'id':'places_area__row'})
# 通过父标签再来定位子标签
td = tr.find(attrs={'class':'w2p_fw'})
area = td.text
print("面积为:", area)

