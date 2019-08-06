import logging
#ip初始评分
MAX_SCORE=50
#日志默认配置
LOG_LEVEL=logging.INFO #默认级别
LOG_FMT='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
LOG_DATEFMT='%Y-%M-%d %H:%M:%S'
LOG_FILENAME='log.log'

#测试代理的ip超时时间
TEST_TIMEOUT=15

#MongoDB的数据的的URL
MONGO_URL='mongodb://127.0.0.1:27017'
#获取每个网页的间隔
SLEEP_TIME=1

# 配置代理爬虫列表
PROXIES_SPIDERS = [
    'core.proxy_spider.proxy_spider.IphaiSpider',
    'core.proxy_spider.proxy_spider.XiciSpider',
    'core.proxy_spider.proxy_spider.ProxylistplusSpider',
]

#爬虫的时间间隔
RUN_SPIDERS_INTERVAL=12

#用于配置检测代理ip的异步数量
TEST_PROXIES_ASYNC_COUNT=10

#检测代理ip的时间间隔
RUN_PROXY_TEST_INTERVAL=2

#获取最大IP的数量；值越下，可以信越高，随机性就越差
PROXIES_MAX_COUNT=10