# -*- coding: utf-8 -*-


class WeixinSogouException(Exception):
    """基于搜狗搜索的的微信爬虫接口  异常类
    """

    def __init__(self, message, code=500):
        self.code = code
        self.message = message
        Exception(message)


class AntiSpiderException(WeixinSogouException):
    """
    反爬虫异常
    """
    pass
