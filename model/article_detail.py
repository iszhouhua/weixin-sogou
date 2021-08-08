# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel, Field


class OfficialAccount(BaseModel):
    wechat_name: str = Field(None, title='公众号名称')
    wechat_id: str = Field(None, title='微信号')
    qr_code: str = Field(None, title='临时二维码')
    introduction: str = Field(None, title='介绍')


class ArticleDetail(BaseModel):
    title: str = Field(None, title='文章标题')
    copyright: str = Field(None, title='版权')
    author: str = Field(None, title='作者')
    time: str = Field(None, title='发布时间')
    temp_url: str = Field(None, title='临时链接')
    content_text: str = Field(None, title='微信文本内容')
    content_img_list: List[str] = Field([], title='微信文本中图片列表')
    content_html: str = Field(None, title='微信原文内容')
    official_account: OfficialAccount = Field(None, title='公众号信息')
