import random
from pymongo import MongoClient
import pymongo
from  settings import MONGO_URL
from utils.log import logger
from domain import Proxy
"""
数据库模块
"""


class MongoPool(object):
    def __init__(self):
        #建立数据连接，获取要操作的集合
        self.client=MongoClient(MONGO_URL)
        #获取要操作的集合
        self.proxies=self.client['proxy_pool']['proxies']

    def __del__(self):
        #关闭数据的连接
        self.client.close()

    def insert_one(self,proxy):
        # 插入
        count=self.proxies.count_documents({'_id':proxy.ip})
        if count==0:
            #使用ip作为主键:_id
            dic=proxy.__dict__
            dic['_id']=proxy.ip
            self.proxies.insert_one(dic)
            logger.info("插入新的代理:{}".format(proxy))
        else:
            logger.warning("已经存在代理:{}".format(proxy))

    def update_one(self,proxy):
        # 修改
        self.proxies.update_one({'_id':proxy.ip},{"$set":proxy.__dict__})

    def delete_one(self,proxy):
        #删除
        self.proxies.delete_one({'_id':proxy.ip})
        logger.info("删除代理:{}".format(proxy))

    def find_all(self):
        #查询所有
        cursor=self.proxies.find()
        for item in cursor:
            #item中有_id proxy没有
            item.pop('_id')
            proxy=Proxy(**item)
            yield proxy

    def find(self,conditions={},count=0):
        """
        根据条件进行查询
        :param conditions:查询条件字典
        :param count: 限制最多取出多少个ip
        :return: 返回满足要求的ip列表
        """
        cursor=self.proxies.find(conditions,limit=count).\
            sort([('score',pymongo.DESCENDING),('speed',pymongo.ASCENDING)])
        #准备列表用于存储指针
        proxy_list=[]
        for item in cursor:
            item.pop('_id')
            proxy=Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self,protocol,domain,count=0,nick_type=2):
        """
        实现根据协议类型 和访问网址域名，获取ip列表
        :param protocal: http,https
        :param domain: 域名：jd.com
        :param count: 用于限制ip数量
        :param nick_type: 匿名类型，默认获取高匿的ip
        :return: 返回满足要求的代理ip
        """
        #定义一个查询条件
        conditions={'nick_type':nick_type}
        #判断协议类型
        if protocol is None:
            #如果没有传入协议类型返回http，https双类型
            conditions['protocol']=2
        elif protocol.lower()=='http':
            conditions['protocol']={'$in':[0,2]}
        else:
            conditions['protocol'] = {'$in': [1, 2]}

        if domain:
            conditions['disable_domains']={'$nin':[domain]}
        return  self.find(conditions=conditions,count=count)

    def random_proxy(self,protocol=None,domain=None,count=1,nick_type=0):
        """
        随机产生一个ip
        :param protocal: http,https
        :param domain: 域名：jd.com
        :param count: 用于限制ip数量
        :param nick_type: 匿名类型，默认获取高匿的ip
        :return: 返回满足要求的随机的一个代理ip
        """
        proxy_list=self.get_proxies(protocol=protocol,domain=domain,count=count,nick_type=nick_type)
        return random.choice(proxy_list)

    def disable_domain(self,ip,domain):
        """
        把指定域名添加到ip的不可访问域
        :param ip: ip地址
        :param domain: 域名
        :return: True添加成功，False添加失败
        """
        #判断不可访问域名中有无该域名
        if self.proxies.count_documents({'_id':ip,'disable_domain':domain})==0:
            self.proxies.update_one({'_id':ip},{'$push':{'disable_domain':domain}})
            return True
        return False

if __name__=="__main__":
    mongo=MongoPool()
    # proxy = Proxy('203.42.227.113', port='8080')
    # mongo.insert_one(proxy)
    # proxy = Proxy('203.42.227.113', port='8888')
    # mongo.update_one(proxy)
    #proxy = Proxy('203.42.227.113', port='8888')
    #mongo.delete_one(proxy)
    # for i in mongo.find_all():
    #     print(i)
    proxy =mongo.get_proxies(protocol='http',domain='',count=20)
    for p in proxy:
        print(p)