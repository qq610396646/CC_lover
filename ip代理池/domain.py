from settings import MAX_SCORE
class Proxy(object):
    def __init__(self,ip,port,protocol=-1,nick_type=-1,speed=-1,area=None,score=MAX_SCORE,disable_domain=[]):
        """
        ip:ip地址
        port:ip端口
        protocol:支持协议，0->http,1->https,2->http,https
        nick_type:匿名程度，0->高匿,1->匿名,2->透明
        speed:响应速度s
        area:ip所在区域
        score:ip评分,越低越差
        disable_domain:ip不可以用领域
        """
        self.ip=ip
        self.port=port
        self.protocol=protocol
        self.nick_type=nick_type
        self.speed=speed
        self.area=area
        self.score=score
        self.disable_domain=disable_domain

    def __str__(self):
        return str(self.__dict__)

