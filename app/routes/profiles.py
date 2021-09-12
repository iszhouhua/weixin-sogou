from typing import List

from fastapi import APIRouter, Query

from ..model.profile_detail import ProfileDetail
from ..model.profile_list import ProfileList
from ..model.response import Result
from ..spider import spider
from ..config import TYPE_PROFILE

router = APIRouter()


@router.get("/search", summary="公众号搜索", response_model=Result[List[ProfileList]])
async def profile_search(keyword: str = Query(..., title='关键字', description='搜索关键字'),
                         page: int = Query(1, title='页码', description='搜索页码')):
    return Result(data=spider.search(keyword, page, TYPE_PROFILE))


@router.get("/detail", summary="公众号详情", response_model=Result[ProfileDetail])
async def article_detail(url: str = Query(..., title='临时链接', description='搜狗或微信的临时链接',
                                          regex=r'^http(s?)://(mp\.)?weixin\.(sogou|qq)\.com/+')):
    return Result(data=spider.get_detail(url, TYPE_PROFILE))
