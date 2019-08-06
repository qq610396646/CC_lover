from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import importlib
import time
import schedule

from settings import PROXIES_SPIDERS,RUN_SPIDERS_INTERVAL
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger

class RunSpider(object):

    def __init__(self):
        self.mongo_pool=MongoPool()
        self.coroutine_pool=Pool()

    def run(self):
        spiders=self.get_spider_from_settings()
        for spider in spiders:
            #异步的方式
            self.coroutine_pool.apply_async(self._execute_one_spider,args=(spider,))
        self.coroutine_pool.join()

    def _execute_one_spider(self, spider):
        try:
            for proxy in spider.get_proxies():
                # 检验ip
                proxy = check_proxy(proxy)
                # speed=-1不可以
                if proxy.speed != -1:
                    self.mongo_pool.insert_one(proxy)
        except Exception as ex:
            logger.exception(ex)

    def get_spider_from_settings(self):
        # 根据配置文件获取爬虫列表
        for full_class_name in PROXIES_SPIDERS:
            #获取模块名和类名
            module_name,class_name=full_class_name.rsplit('.',maxsplit=1)
            #根据模块名导入模块 ---->import proxy_spider
            module=importlib.import_module(module_name)
            #根据类名，从模块中获取类---->from proxy_spider import ProxylistplusSpider,
            cls=getattr(module,class_name)
            spider=cls()
            yield spider

    @classmethod
    def start(cls):
        r = RunSpider()
        r.run()
        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(r.run())
        while True:
            schedule.run_pending()
            time.sleep(3600)

if __name__ == '__main__':
    RunSpider.start()