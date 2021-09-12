from typing import List

from fastapi import APIRouter, Query

from ..config import TYPE_ARTICLE
from ..model.article_detail import ArticleDetail
from ..model.article_list import ArticleList
from ..model.response import Result
from ..spider import spider

router = APIRouter()


@router.get("/search", summary="文章搜索", response_model=Result[List[ArticleList]])
async def article_search(keyword: str = Query(..., title='关键字', description='搜索关键字'),
                         page: int = Query(1, title='页码', description='搜索页码')):
    return Result(data=spider.search(keyword, page, TYPE_ARTICLE))


@router.get("/detail", summary="文章详情", response_model=Result[ArticleDetail])
async def article_detail(url: str = Query(..., title='临时链接', description='搜狗或微信的临时链接', example='',
                                          regex=r'^http(s?)://(mp\.)?weixin\.(sogou|qq)\.com/+')):
    return Result(data=spider.get_detail(url))
