# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import logging
import random
import re
from urllib.parse import urlencode

import requests
from . import parse
from .exceptions import WeixinSogouException, AntiSpiderException
from ..config import SOGOU_BASE_URL, HEADERS, TYPE_ARTICLE


def refresh_cookie():
    """
    刷新搜狗cookie
    """
    qs_dict = {
        'type': TYPE_ARTICLE,
        's_from': 'input',
        'query': chr(random.randint(0x4e00, 0x9fbf)),
        'page': 1,
        'ie': 'utf8'
    }
    url = f'{SOGOU_BASE_URL}/weixin?{urlencode(qs_dict)}'
    resp = get(url)
    suid = resp.cookies.get("SUID")
    snuid = resp.cookies.get("SNUID")
    HEADERS["Cookie"] = f"SNUID={snuid};SUID={suid};"


def get(url, is_retry=True):
    """发送请求

    Parameters
    ----------
    url : str
        请求的链接
    is_retry : bool, optional
        遭遇反爬虫时是否重试
    """
    resp = requests.get(url, headers=HEADERS)
    if not resp.ok:
        raise WeixinSogouException('搜狗接口请求失败.url:{}'.format(url), resp.status_code)
    elif 'antispider' in resp.url:
        if is_retry:
            # 刷新cookie，重试一次
            refresh_cookie()
            return get(url, False)
        raise AntiSpiderException('被搜狗识别为异常请求.', 403)
    resp.encoding = 'utf-8'
    return resp


def search(keyword, page=1, search_type=TYPE_ARTICLE):
    """搜索 文章

    Parameters
    ----------
    keyword : str or unicode
        搜索文字
    search_type : int, optional
        搜索类型 the default is 2
    page : int, optional
        页数 the default is 1

    Returns
    -------
    list[ArticleList]
    or
    list[OfficialAccountList]

    Raises
    ------
    WeixinSogouException
        requests error
    """

    qs_dict = {
        'type': search_type,
        's_from': 'input',
        'query': keyword,
        'page': page,
        'ie': 'utf8'
    }
    url = f'{SOGOU_BASE_URL}/weixin?{urlencode(qs_dict)}'
    resp = get(url)
    data_list = parse.get_article_by_search(resp.text) \
        if search_type == TYPE_ARTICLE \
        else parse.get_profile_by_search(resp.text)
    if not data_list:
        logging.info(f"关键字【{keyword}】,第{page}页搜索内容为空.search_type:{search_type}")
    return data_list


def get_detail(url, request_type=TYPE_ARTICLE):
    """根据临时链接获取文章内容

    Parameters
    ----------
    url : str or unicode
        原文链接，临时链接
    request_type: int, optional
        链接类型 the default is 2
    Returns
    -------
    ArticleDetail

    Raises
    ------
    WeixinSogouException
    """
    if re.match(r'http(s?)://weixin\.sogou\.com/', url):
        # 搜狗URL得到的是js脚本，需要解析链接去请求微信
        resp = get(url)
        url = parse.get_wechat_url(resp.text)
    resp = get(url)
    parse.check_weixin_error(resp.text)
    content_info = parse.get_article_detail(resp.text) \
        if request_type == TYPE_ARTICLE \
        else parse.get_profile_detail(resp.text)
    content_info.temp_url = resp.url
    return content_info
