# -*- coding: utf-8 -*-
from typing import Generic, TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class Result(GenericModel, Generic[DataT]):
    code: int = Field(200, title='错误码', description='200表示成功返回，其余为失败')
    message: str = Field('OK', title='错误描述', description='出错时的错误描述')
    data: DataT = Field(None, title='数据', description='成功时的响应数据')
