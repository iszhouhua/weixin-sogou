# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from app.handler.error_handler import service_error_handler, validation_error_handler, weixin_error_handler

from app.handler.middleware_handler import http_middleware
from app.routes import articles, profiles
from app.spider.exceptions import WeixinSogouException


def create_app() -> FastAPI:
    application = FastAPI(title="搜狗微信搜索爬虫",
                          description="基于搜狗微信搜索的爬虫接口",
                          version="1.0.0"
                          )
    application.add_exception_handler(Exception, service_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)
    application.add_exception_handler(WeixinSogouException, weixin_error_handler)
    application.add_middleware(BaseHTTPMiddleware, dispatch=http_middleware)
    application.include_router(articles.router, tags=["文章"], prefix="/article")
    application.include_router(profiles.router, tags=["公众号"], prefix="/profile")
    return application


app = create_app()
