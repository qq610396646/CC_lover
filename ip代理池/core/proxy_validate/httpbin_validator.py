import  time
import requests
import json

from utils.http import get_request_header
from settings import TEST_TIMEOUT
from utils.log import logger
from domain import Proxy
"""
校验模块
1 ip速度
2 匿名程度
3 支持ip协议类型
"""
def check_proxy(proxy):
    """
    用于检测指定ip
    :param proxy:代理ip
    :return:检测后的代理ip对象
    """
    proxies={
        "http":'http://{}:{}'.format(proxy.ip,proxy.port),
        "https": 'https://{}:{}'.format(proxy.ip, proxy.port)
    }
    # 测试代理ip
    http,http_nick_type,http_speed=__check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies,False)

    if http and https:
        proxy.protocol=2
        proxy.nick_type=https_nick_type
        proxy.speed=https_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed =-1

    logger.info(proxy)
    return proxy

def __check_http_proxies(proxies,is_http=True):
    # 默认无法识别的匿名程度
    nick_type=-1
    # 默认无法响应的速度
    speed=-1

    if is_http:
        test_url="http://httpbin.org/get"
    else:
        test_url = "https://httpbin.org/get"

    try:
        # 获取开始时间
        start=time.time()
        # 发送请求获取响应数据
        response=requests.get(test_url,headers=get_request_header(),proxies=proxies,timeout=TEST_TIMEOUT)

        if response.ok:
            # 计算响应速度
            speed=round(time.time()-start,2)
            # 匿名程度
            dic=json.loads(response.text)
            # 把jason字符串转换成字典
            # 获取origin->来源的ip
            origin=dic["origin"]
            proxy_connection=dic['headers'].get('Proxy-Connetion',None)
            if ',' in origin:
                nick_type=2
            elif proxy_connection:
                nick_type=1
            else:
                nick_type=0
            return True,nick_type,speed
        return False,nick_type,speed
    except Exception as e:
        #logger.exception(e)
        return False, nick_type, speed

if __name__=="__main__":
    proxy=Proxy('203.42.227.113',port='8080')
    print(check_proxy(proxy))