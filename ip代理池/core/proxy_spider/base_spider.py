import requests
from lxml import html
from utils.http import get_request_header
from domain import Proxy
import time
from settings import SLEEP_TIME

class BaseSpider(object):
    urls = []  # 代理IP网址的URL的列表
    group_xpath = ''  # 分组XPATH, 获取包含代理IP信息标签列表的XPATH
    detail_xpath = {}  # 组内XPATH, 获取代理IP详情的信息XPATH
    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        """
        通用爬虫
        :param urls:网址列表
        :param group_xpath: 表格
        :param detail_xpath: 表格中的单项
        """
        if urls:  # 如果urls中有数据
            self.urls = urls
        if group_xpath:  # 如果group_xpath中有数据
            self.group_xpath = group_xpath
        if detail_xpath:  # 如果detail_xpath中有数据
            self.detail_xpath = detail_xpath

    def get_page_from_url(self,url):
        #获取页面数据
        response=requests.get(url,headers=get_request_header())
        return response.content

    def get_first_from_list(self,lis):
        return lis[0].strip() if len(lis) != 0 else ''

    def get_proxies_from_page(self,page):
        #解析页面，获取数据
        element=html.etree.HTML(page)
        #获取ip的标签列表
        trs=element.xpath(self.group_xpath)
        for tr in trs:
            ip=self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port=self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area=self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            if ip =='' or  port =='':
                continue
            proxy=Proxy(ip=ip,port=port,area=area)
            #用yield返回
            yield proxy

    def get_proxies(self):
        # 对外获取ip
        for url in self.urls:
            #获取页面数据
            page = self.get_page_from_url(url)
            time.sleep(SLEEP_TIME)
            #解析页面
            proxies=self.get_proxies_from_page(page)
            #返回proxy对象
            yield from proxies

if __name__=="__main__":
    config={
        'urls':['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1,2)],
        'group_xpath':'//*[@id="ip_list"]//tr',
        'detail_xpath':{
            'ip':'./td[2]/text()',
            'port':'./td[3]/text()',
            'area':'./td[4]/a/text()'
        }
    }

    spider=BaseSpider(**config)
    for p in spider.get_proxies():
        print(p)