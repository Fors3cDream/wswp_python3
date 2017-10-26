import urllib.robotparser
import urllib.parse

def getRobots(url):
    """
    初始化robots.txt解析器
    :param url:
    :return:
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp