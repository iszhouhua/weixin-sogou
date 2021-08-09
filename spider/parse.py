# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import re
from lxml import etree

from model import article_list, article_detail
from .const import WEIXIN_BASE_URL, SOGOU_BASE_URL
from .exceptions import WeixinSogouException
from .utils import get_first_elem, format_url, get_elem_text, format_time


def check_sogou_error(text):
    page = etree.HTML(text)
    error_msg = ''.join(page.xpath('//div[@class="text-info"]//text()'))
    if error_msg:
        raise WeixinSogouException(error_msg, 410)


def check_weixin_error(text):
    html = etree.HTML(text)
    error_msg = get_elem_text(html, '//div[@class="weui-msg"]/div[@class="weui-msg__text-area"]//text()')
    if error_msg:
        raise WeixinSogouException(error_msg, 410)


def get_wechat_url(text):
    """
    从js脚本中解析文章详情页链接
    """
    uri = ''
    base_url = re.findall(r'var url = \'(.*?)\';', text)
    if base_url and len(base_url) > 0:
        uri = base_url[0]

    mp_url = re.findall(r'url \+= \'(.*?)\';', text)
    if mp_url:
        uri = uri + ''.join(mp_url)
    url = uri.replace('@', '')
    return url


def get_article_by_search(text):
    """从搜索文章获得的文本 提取章列表信息

    Parameters
    ----------
    text : str or unicode
        搜索文章获得的文本

    Returns
    -------
    list[ArticleList]
    """
    page = etree.HTML(text)
    lis = page.xpath('//ul[@class="news-list"]/li')

    articles = []
    for li in lis:
        url = get_first_elem(li, 'div[1]/a/@href')
        if url:
            title = get_elem_text(li, 'div[2]/h3/a/text()')
            imgs = [format_url(get_first_elem(li, 'div[1]/a/img/@src'), "https:")]
            abstract = get_elem_text(li, 'div[2]/p//text()')
            time = get_first_elem(li, 'div[2]/div/span/script/text()')
            gzh_info = get_first_elem(li, 'div[2]/div/a')
        else:
            url = get_first_elem(li, 'div/h3/a/@href')
            title = get_elem_text(li, 'div/h3/a/@text()')
            imgs = []
            spans = li.xpath('div/div[1]/a')
            for span in spans:
                img = get_first_elem(span, 'span/img/@src')
                if img:
                    imgs.append(format_url(img, "https:"))
            abstract = get_elem_text(li, 'div/p//text()')
            time = get_first_elem(li, 'div/div[2]/span/script/text()')
            gzh_info = get_first_elem(li, 'div/div[2]/a')

        time = re.search(r'timeConvert\(\'(.*?)\'\)', time)
        time = format_time(time.group(1)) if time else None
        profile_url = get_first_elem(gzh_info, '@href')
        head_image = get_first_elem(gzh_info, '@data-headimage')
        wechat_name = get_first_elem(gzh_info, 'text()')
        gzh_isv = get_first_elem(gzh_info, '@data-isv')

        articles.append(article_list.ArticleList(
            article=article_list.Article(
                title=title,
                url=format_url(url, SOGOU_BASE_URL),
                img_list=imgs,
                abstract=abstract,
                time=time
            ),
            official_account=article_list.OfficialAccount(
                profile_url=format_url(profile_url, SOGOU_BASE_URL),
                head_image=head_image,
                wechat_name=wechat_name,
                authentication=int(gzh_isv),
            )
        ))
    return articles


def get_article_detail(text):
    """获取微信文章明细

    1. 获取文本中所有的图片链接列表
    2. 获取微信文章的html内容页面(去除标题等信息)

    Parameters
    ----------
    text : str or unicode
        一篇微信文章的文本

    Returns
    -------
    ArticleDetail
    """
    detail = etree.HTML(text)
    title = get_elem_text(detail, '//h2[@id="activity-name"]/text()')
    time_search = re.search(r'<script(.*)n="(.*?)"(.*)document\.getElementById\(\"publish_time\"\)', text, re.S)
    publish_time = format_time(time_search.group(2)) if time_search else ''
    # 获取微信meta
    mate_content = get_first_elem(detail, '//div[@id="meta_content"]')
    copyright = get_elem_text(mate_content, 'span[@id="copyright_logo"]/text()')
    author = get_elem_text(mate_content, 'span[contains(@class,"rich_media_meta_text")]//text()')
    # 获取公众号信息
    oa_info = get_first_elem(detail, '//div[@id="js_profile_qrcode"]')
    wechat_name = get_elem_text(oa_info, 'div/strong[@class="profile_nickname"]/text()')
    wechat_id = get_elem_text(oa_info, 'div/p[1]/span/text()')
    introduction = get_elem_text(oa_info, 'div/p[2]/span/text()')

    qr_code = re.search(r'window.sg_qr_code=\"(.*?)\"', text)
    qr_code = format_url(qr_code.group(1).replace('\\x26amp;', '&'), WEIXIN_BASE_URL) if qr_code else None
    # 获取微信文本content
    content = get_first_elem(detail, '//div[@id="js_content"]')
    content_text = get_elem_text(content, './/text()')
    img_list = content.xpath('.//img/@data-src')
    return article_detail.ArticleDetail(
        title=title,
        author=author,
        time=publish_time,
        copyright=copyright,
        content_img_list=img_list,
        content_text=content_text,
        content_html=etree.tostring(content, encoding='utf-8'),
        official_account=article_detail.OfficialAccount(
            qr_code=qr_code,
            wechat_name=wechat_name,
            wechat_id=wechat_id,
            introduction=introduction,
        )
    )
