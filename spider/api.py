# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import random
import re
from time import sleep
from urllib.parse import urlencode

import requests

from model.article_detail import ArticleDetail
from spider import const, parse
from spider.const import SOGOU_BASE_URL
from spider.exceptions import WeixinSogouException, AntiSpiderException


class SpiderApi(object):
    def __init__(self):
        self.cookies = None

    def __get(self, url):
        resp = requests.get(url, headers=const.headers, cookies=self.cookies)

        if not resp.ok:
            raise WeixinSogouException('搜狗接口请求失败.url:{}'.format(url), resp.status_code)
        elif 'antispider' in resp.url:
            # 被抓了，清除cookie
            self.cookies = None
            raise AntiSpiderException('被搜狗识别为异常请求,请稍后再试.', 403)
        resp.encoding = 'utf-8'
        return resp

    def search_article(self, keyword, page=1):
        """搜索 文章

        Parameters
        ----------
        keyword : str or unicode
            搜索文字
        page : int, optional
            页数 the default is 1

        Returns
        -------
        list[ArticleList]

        Raises
        ------
        WeixinSogouException
            requests error
        """

        qs_dict = {
            'type': 2,
            's_from': 'input',
            'query': keyword,
            'page': page,
            'ie': 'utf8'
        }
        url = f'{SOGOU_BASE_URL}/weixin?{urlencode(qs_dict)}'
        resp = self.__get(url)
        if resp.cookies:
            self.cookies = resp.cookies
        parse.check_sogou_error(resp.text)
        return parse.get_article_by_search(resp.text)

    def get_article_content(self, url):
        """根据临时链接获取文章内容

        Parameters
        ----------
        url : str or unicode
            原文链接，临时链接

        Returns
        -------
        ArticleDetail

        Raises
        ------
        WeixinSogouException
        """
        if re.match(r'http(s?)://weixin\.sogou\.com/', url):
            try:
                resp = self.__get(url)
            except AntiSpiderException:
                # 搜狗反爬机制需要搜索之后才能访问详情，未搜索直接访问需要输入验证码，生成随机内容搜索一次
                val = chr(random.randint(0x4e00, 0x9fbf))
                self.search_article(val)
                sleep(1)
                resp = self.__get(url)
            # 搜狗URL得到的是js脚本，需要解析链接去请求微信
            url = parse.get_wechat_url(resp.text)
        resp = self.__get(url)
        parse.check_weixin_error(resp.text)
        content_info = parse.get_article_detail(resp.text)
        content_info.temp_url = resp.url
        return content_info
