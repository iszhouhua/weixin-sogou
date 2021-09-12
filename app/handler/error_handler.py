from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import validation_error_response_definition
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.config import logger
from app.model.response import Result
from app.spider.exceptions import WeixinSogouException


async def service_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error('出现未知错误，请求地址：{},参数:{}'.format(request.url, request.query_params), exc_info=exc)
    content = jsonable_encoder(Result(code=500, message='服务器异常'))
    return JSONResponse(content)


async def weixin_error_handler(request: Request, exc: WeixinSogouException) -> JSONResponse:
    logger.error('请求出错，请求地址：{},参数:{},描述:{}'.format(request.url, request.query_params, exc.message), exc_info=exc)
    content = jsonable_encoder(Result(code=exc.code, message=exc.message))
    return JSONResponse(content)


async def validation_error_handler(request: Request, exc: RequestValidationError):
    logger.warning('请求参数非法，请求地址：{},参数:{},errors:{}'.format(request.url, request.query_params, str(exc)))
    content = jsonable_encoder(
        Result(code=HTTP_422_UNPROCESSABLE_ENTITY, message='.\n'.join([err['msg'] for err in exc.errors()])))
    return JSONResponse(content, status_code=HTTP_422_UNPROCESSABLE_ENTITY)


validation_error_response_definition["properties"] = {
    "code": {"type": "number", "default": "422"},
    "message": {"type": "string"}
}
