import logging
import time

from starlette.requests import Request


async def http_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info('request ip = %s , url = %s(%s) ,consume time = %.3fs, queryString = %s',
                 request.client.host, request.url, request.method, process_time, request.query_params)
    return response
