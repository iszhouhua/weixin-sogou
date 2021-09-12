# -*- coding: utf-8 -*-
import json
import logging.config
import os

SOGOU_BASE_URL = "https://weixin.sogou.com"

WEIXIN_BASE_URL = "https://mp.weixin.qq.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/92.0.4515.107 Safari/537.36",
    "Referer": SOGOU_BASE_URL,
    "Cookie": ""
}

TYPE_PROFILE = 1  # 公众号
TYPE_ARTICLE = 2  # 文章

logging_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'logger_config.json'
with open(logging_path) as file:
    loaded_config = json.load(file)
    logging.config.dictConfig(loaded_config)
logger = logging.getLogger("weixin-sogou")
