import requests
import re
import js2py

from base_spider import BaseSpider
from utils.http import get_request_header
from domain import Proxy

"""
西刺代理:`http://www.xicidaili.com/nn/1`
"""
class XiciSpider(BaseSpider):
    urls = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 10)]
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    detail_xpath = {'ip': './td[2]/text()', 'port': './td[3]/text()', 'area': './td[4]/a/text()'}

"""
ip嗨代理:`http://www.iphai.com/free/ng`
"""
class IphaiSpider(BaseSpider):
    urls = ['http://www.iphai.com/free/ng', 'http://www.iphai.com/free/wg']
    group_xpath = '//table/tr[position()>1]'
    detail_xpath = {'ip':'./td[1]/text()', 'port':'./td[2]/text()', 'area':'./td[5]/text()' }

"""
proxylistplus爬虫: `https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1`
"""
class ProxylistplusSpider(BaseSpider):
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1, 7)]
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
    detail_xpath = {'ip':'./td[2]/text()', 'port':'./td[3]/text()', 'area':'./td[5]/text()'}


if __name__ == '__main__':
    #spider = XiciSpider()
    #spider = IphaiSpider()
    spider = ProxylistplusSpider()

    for proxy in spider.get_proxies():
        print(proxy)