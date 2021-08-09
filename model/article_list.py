# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel, Field


class Profile(BaseModel):
    wechat_name: str = Field(None, title='公众号名称')
    head_image: str = Field(None, title='公众号头像')
    profile_url: str = Field(None, title='公众号链接(临时)')
    is_verify: bool = Field(None, title='认证状态')


class Article(BaseModel):
    title: str = Field(None, title='文章标题')
    url: str = Field(None, title='文章链接(临时)')
    img_list: List[str] = Field([], title='文章图片')
    time: str = Field(None, title='搜狗收录时间')
    abstract: str = Field(None, title='文章摘要')


class ArticleList(BaseModel):
    article: Article = Field(None, title='文章信息')
    profile: Profile = Field(None, title='公众号信息')
