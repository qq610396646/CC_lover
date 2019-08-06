from multiprocessing import Process
from core.proxy_spider.run_spider import  RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import Proxy_Api
def run():
    # 定义一个列表，启动进程
    process_list=[]
    # 创建爬虫的进程
    process_list.append(Process(target=RunSpider.start, name='run_spider'))
    process_list.append(Process(target=ProxyTester.start, name='run_tester'))
    #process_list.append(Process(target=Proxy_Api.start, name='run_api'))

    #启动子进程
    for process in process_list:
        #守护进程
        process.daemon=True
        process.start()

    for process in process_list:
        #守护进程
        process.join()


if __name__ == '__main__':
    run()

