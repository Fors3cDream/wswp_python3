from wswp_1_pro.downloader import download
import lxml.html

url = 'http://example.webscraping.com/places/default/view/China-47'

html = download(url, headers={'User-agent':'wswp'}, proxy=None, numRetries=2)

tree = lxml.html.fromstring(str(html))


# 从面积的父标签开始提取内容
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
# td1 = tree.xpath('//tr[@id="places_area__row"]/td[@class="w2p_fw"]')[0]
area = td.text_content()
# area1 = td1.text_content()
print("面积为：", area)