# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel, Field


class ProfileDetail(BaseModel):
    temp_url: str = Field(None, title='公众号链接(临时)')
    head_image: str = Field(None, title='公众号头像')
    wechat_name: str = Field(None, title='公众号名称')
    wechat_id: str = Field(None, title='微信号')
    qr_code: str = Field(None, title='临时二维码')
    introduction: str = Field(None, title='介绍')
    is_verify: bool = Field(None, title='认证状态')
    verify_company: str = Field(None, title='账号主体')
