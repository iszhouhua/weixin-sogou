# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import re
from lxml import etree

from .exceptions import AntiSpiderException, WeixinSogouException
from ..model import article_list, article_detail, profile_list, profile_detail
from ..config import WEIXIN_BASE_URL, SOGOU_BASE_URL
from .utils import get_first_elem, format_url, get_elem_text, format_time


def check_weixin_error(text):
    if '为了保护你的网络安全，请输入验证码' in text:
        raise AntiSpiderException('被微信识别为异常请求.', 403)
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
    """提取文章列表信息

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
            title = get_elem_text(li, 'div[2]/h3/a//text()')
            imgs = [format_url(get_first_elem(li, 'div[1]/a/img/@src'), "https:")]
            abstract = get_elem_text(li, 'div[2]/p//text()')
            time = get_first_elem(li, 'div[2]/div/span/script/text()')
            profile_info = get_first_elem(li, 'div[2]/div/a')
        else:
            url = get_first_elem(li, 'div/h3/a/@href')
            title = get_elem_text(li, 'div/h3/a//text()')
            imgs = []
            spans = li.xpath('div/div[1]/a')
            for span in spans:
                img = get_first_elem(span, 'span/img/@src')
                if img:
                    imgs.append(format_url(img, "https:"))
            abstract = get_elem_text(li, 'div/p//text()')
            time = get_first_elem(li, 'div/div[2]/span/script/text()')
            profile_info = get_first_elem(li, 'div/div[2]/a')

        time = re.search(r'timeConvert\(\'(.*?)\'\)', time)
        time = format_time(time.group(1)) if time else None
        profile_url = get_first_elem(profile_info, '@href')
        head_image = get_first_elem(profile_info, '@data-headimage')
        wechat_name = get_first_elem(profile_info, 'text()')
        profile_isv = get_first_elem(profile_info, '@data-isv')
        is_verify = True if profile_isv and int(profile_isv) == 1 else False

        articles.append(article_list.ArticleList(
            article=article_list.Article(
                title=title,
                url=format_url(url, SOGOU_BASE_URL),
                img_list=imgs,
                abstract=abstract,
                time=time
            ),
            profile=article_list.Profile(
                profile_url=format_url(profile_url, SOGOU_BASE_URL),
                head_image=head_image,
                wechat_name=wechat_name,
                is_verify=is_verify,
            )
        ))
    return articles


def get_profile_by_search(text):
    """提取公众号列表信息

    Parameters
    ----------
    text : str or unicode
        搜索文章获得的文本

    Returns
    -------
    list[ArticleList]
    """
    page = etree.HTML(text)
    lis = page.xpath('//ul[@class="news-list2"]/li')
    relist = []
    for li in lis:
        open_id = get_first_elem(li, '@d')
        url = format_url(get_first_elem(li, 'div/div[1]/a/@href'), SOGOU_BASE_URL)
        head_image = format_url(get_first_elem(li, 'div/div[1]/a/img/@src'), "https:")
        wechat_name = get_elem_text(li, 'div/div[2]/p[1]//text()')
        wechat_id = get_elem_text(li, 'div/div[2]/p[2]/label/text()')
        qr_code = format_url(get_first_elem(li, 'div/div[4]/span/img[1]/@src'), 'https:')
        recent_article = None
        introduction = ''
        authentication = ''
        for node in li.xpath('dl'):
            desc = get_elem_text(node, 'dt/text()')
            if '功能介绍' in desc:
                introduction = get_elem_text(node, 'dd//text()')
            elif '认证' in desc:
                authentication = get_elem_text(node, 'dd/text()')
            elif '最近文章' in desc:
                article_title = get_elem_text(node, 'dd/a//text()')
                article_url = format_url(get_first_elem(node, 'dd/a/@href'), SOGOU_BASE_URL)
                article_time = get_first_elem(node, 'dd/span/script/text()')
                if article_time:
                    article_time = re.search(r'timeConvert\(\'(.*?)\'\)', article_time)
                    article_time = format_time(article_time.group(1)) if article_time else None
                recent_article = profile_list.RecentArticle(
                    title=article_title,
                    url=article_url,
                    time=article_time
                )

        relist.append(profile_list.ProfileList(
            open_id=open_id,
            profile_url=url,
            head_image=head_image,
            wechat_name=wechat_name,
            wechat_id=wechat_id,
            qr_code=qr_code,
            introduction=introduction,
            verify_company=authentication,
            recent_article=recent_article
        ))
    return relist


def get_article_detail(text):
    """获取微信文章明细

    Parameters
    ----------
    text : str or unicode
        一篇微信文章的文本

    Returns
    -------
    ArticleDetail
    """
    detail = etree.HTML(text)
    title = get_elem_text(detail, '//h1[@id="activity-name"]/text()')
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
        profile=article_detail.Profile(
            qr_code=qr_code,
            wechat_name=wechat_name,
            wechat_id=wechat_id,
            introduction=introduction,
        )
    )


def get_profile_detail(text):
    """
    获取微信公众号信息

    Parameters
    ----------
    text : str or unicode
        公众号详情页内容

    Returns
    -------
    OfficialAccountInfo
    """
    detail = etree.HTML(text)
    profile_info = get_first_elem(detail, '//div[@class="profile_info_area"]')
    head_image = get_first_elem(profile_info, 'div/span/img/@src')
    wechat_id = get_elem_text(profile_info, 'div/div/p/text()').replace('微信号: ', '')
    wechat_name = get_elem_text(profile_info, 'div/div/strong/text()')
    qr_code = format_url(get_first_elem(detail, '//img[@id="js_pc_qr_code_img"]/@src'), WEIXIN_BASE_URL)
    introduction = get_elem_text(profile_info, 'ul/li[1]/div/text()')
    is_verify = True if profile_info.xpath('ul/li[2]/div/img') else False
    verify_company = None
    if is_verify:
        verify_company = get_elem_text(profile_info, 'ul/li[2]/div/text()')
    return profile_detail.ProfileDetail(
        qr_code=qr_code,
        head_image=head_image,
        wechat_name=wechat_name,
        wechat_id=wechat_id,
        introduction=introduction,
        is_verify=is_verify,
        verify_company=verify_company
    )
