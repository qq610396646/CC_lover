from flask import Flask, jsonify
from flask import request
import json
from db.mongo_pool import MongoPool
from settings import PROXIES_MAX_COUNT

class Proxy_Api(object):
    def __init__(self):
        #初始化一个Flask服务
        self.app=Flask(__name__)
        # 创建MongoPool对象用于操作数据库
        self.mongo_pool=MongoPool()
        @self.app.route('/random')
        def random():
            protocol=request.args.get('protocol')
            domain=request.args.get('domain')
            # 随机返回多个proxy对象
            proxy=self.mongo_pool.random_proxy(protocol,domain,count=PROXIES_MAX_COUNT,nick_type=2)
            #print(proxy)
            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.ip, proxy.port)
            else:
                return '{}:{}'.format( proxy.ip, proxy.port)

        @self.app.route('/proxies')
        def proxies():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')

            proxies=self.mongo_pool.get_proxies(protocol,domain,count=PROXIES_MAX_COUNT)
            #把Proxy对象列表转换成字典才可以转换成json
            proxies=[proxy.__dict__ for proxy in proxies]
            #字典转换成json
            print(json.dumps(proxies))
            return json.dumps(proxies,ensure_ascii=False)

        @self.app.route('/disable_domain')
        def disable_domain():
            ip=request.args.get('ip')
            domain = request.args.get('domain')
            if ip is None:
                return '请提供ip这个参数'
            if domain is None:
                return '请提供domain这个参数'

            self.mongo_pool.disable_domain(ip,domain)
            return '{}禁用域名{}成功'.format(ip,domain)

    def run(self):
        self.app.run('127.0.0.1',port=16889)

    @classmethod
    def start(cls):
        Pa=cls()
        Pa.run()

if __name__ == '__main__':
    Proxy_Api.start()