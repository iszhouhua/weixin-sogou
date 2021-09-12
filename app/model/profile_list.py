# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel, Field


class RecentArticle(BaseModel):
    title: str = Field(None, title='文章标题')
    url: str = Field(None, title='文章链接(临时)')
    time: str = Field(None, title='搜狗收录时间')


class ProfileList(BaseModel):
    open_id: str = Field(None, title='微信号唯一ID')
    profile_url: str = Field(None, title='公众号链接')
    head_image: str = Field(None, title='公众号头像')
    wechat_name: str = Field(None, title='公众号名称')
    wechat_id: str = Field(None, title='微信号')
    qr_code: str = Field(None, title='临时二维码')
    introduction: str = Field(None, title='介绍')
    verify_company: str = Field(None, title='微信认证')
    recent_article: RecentArticle = Field(None, title='最近文章')
