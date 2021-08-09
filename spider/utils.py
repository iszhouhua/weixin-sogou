# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import re
import time


def format_url(url, base):
    if not url:
        return ''
    return base + url if not re.match(r'http(s?)://', url) else url


def format_time(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    if type(timestamp) == str:
        timestamp = int(timestamp)
    struct_time = time.localtime(timestamp)
    return time.strftime(format_str, struct_time)


def get_elem_text(element, path=None):
    """
    获取节点中的文字
    """
    if element is None:
        return ''
    if path:
        element = element.xpath(path)
        if element is None:
            return ''
    return ''.join([node.strip() for node in element])


def get_first_elem(element, path=None):
    """
    获取节点中的首个元素
    """
    if element is None:
        return None
    if path:
        element = element.xpath(path)
    return element[0] if element else None
