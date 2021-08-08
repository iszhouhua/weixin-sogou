# -*- coding: utf-8 -*-
import json
import logging.config
import os
import time
from typing import List
import uvicorn
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from model.article_detail import ArticleDetail
from model.article_list import ArticleList
from model.response import Result
from spider.exceptions import WeixinSogouException
from spider.api import SpiderApi

app = FastAPI(title="搜狗微信搜索爬虫",
              description="基于搜狗微信搜索的爬虫接口",
              version="1.0.0"
              )
spider = SpiderApi()

logging_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'logging.conf'
logging.config.fileConfig(logging_path, disable_existing_loggers=False)
logger = logging.getLogger('spider')


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info('request ip = {} , url = {}({}) ,consume time = {}, queryString = {}'
                .format(request.client.host, request.url, request.method, process_time, request.query_params))
    return response


@app.exception_handler(WeixinSogouException)
async def http_exception_handle(request: Request, exc: WeixinSogouException):
    logger.error('请求出错，请求地址：{},参数:{},描述:{}'.format(request.url, request.query_params, exc.message), exc_info=exc)
    content = jsonable_encoder(Result(code=exc.code, message=exc.message))
    return JSONResponse(content)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning('请求参数非法，请求地址：{},参数:{},errors:{}'.format(request.url, request.query_params, str(exc)))
    content = jsonable_encoder(Result(code=422, message='.\n'.join([err['msg'] for err in exc.errors()])))
    return JSONResponse(content)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error('出现未知错误，请求地址：{},参数:{}'.format(request.url, request.query_params), exc_info=exc)
    content = jsonable_encoder(Result(code=500, message='服务器异常'))
    return JSONResponse(content)


@app.get("/article/search", summary="文章搜索", tags=["文章"], response_model=Result[List[ArticleList]])
async def article_search(keyword: str = Query(..., title='关键字', description='搜索关键字'),
                         page: int = Query(1, title='页码', description='搜索页码')):
    return Result(data=spider.search_article(keyword, page))


@app.get("/article/detail", summary="文章详情", tags=["文章"], response_model=Result[ArticleDetail])
async def article_detail(url: str = Query(..., title='临时链接', description='搜狗或微信的临时链接', example='',
                                          regex=r'^http(s?)://(mp\.)?weixin\.(sogou|qq)\.com/+')):
    return Result(data=spider.get_article_content(url))


# @app.get("/profile/search", summary="公众号搜索", tags=["公众号"])
# async def search(keyword: str, page: int = 1):
#     pass
#
#
# @app.get("/profile/detail", summary="公众号详情", tags=["公众号"])
# async def profile(url: str):
#     """
#     公众号详情
#     """
#     pass


if __name__ == '__main__':
    uvicorn.run("main:app", debug=True, reload=True)