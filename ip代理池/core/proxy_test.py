import time

import schedule
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
from db.mongo_pool import MongoPool
from proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT, RUN_PROXY_TEST_INTERVAL
from utils.log import logger


class ProxyTester(object):
    def __init__(self):
        #创建操作数据库的对象
        self.mongo_pool=MongoPool()
        self.queue=Queue()
        self.corourine_pool=Pool()

    def __check_callback(self,temp):
        self.corourine_pool.apply_async(self.__check_one_proxy,callback=self.__check_callback)

    def __check_one_proxy(self):
        proxy=self.queue.get()
        proxy = check_proxy(proxy)
        if proxy.speed == -1:
            proxy.score -= 1
            if proxy.score <= 0:
                self.mongo_pool.delete_one(proxy)
            else:
                self.mongo_pool.update_one(proxy)
        else:
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        self.queue.task_done()

    def run(self):
        proxies=self.mongo_pool.find_all()
        for proxy in proxies:
            self.queue.put(proxy)
            logger.info(proxy)
        # 开启多个异步
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            self.corourine_pool.apply_async(self.__check_one_proxy(),callback=self.__check_callback)
        self.queue.join()

    @classmethod
    def start(cls):
        pt = cls()
        pt.run()
        schedule.every(RUN_PROXY_TEST_INTERVAL).hours.do(pt.run())
        while True:
            schedule.run_pending()
            time.sleep(3600)


if __name__ == '__main__':
    # pt=ProxyTester()
    # pt.run()
    ProxyTester.start()
