# -*- coding: utf-8 -*-
import logging

import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.main:app", debug=True, reload=True, log_level=logging.DEBUG)
