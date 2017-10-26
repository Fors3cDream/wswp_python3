from wswp_1_pro.downloader import download
import re

url = 'http://example.webscraping.com/places/default/view/China-47'

html = download(url, headers={'User-agent':'wswp'}, proxy=None, numRetries=2)

# for content in re.findall('<td class="w2p_fw">(.*?)</td>', str(html)):
#     print(content)

area = re.findall('<td class="w2p_fw">(.*?)</td>', str(html))[1]
print("面积为:", area)