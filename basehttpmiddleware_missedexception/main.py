import logging
from typing import NoReturn

import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import (
    Response,
    JSONResponse,
)

app = FastAPI()


logger = logging.getLogger(__name__)


@app.get("/raise-exception")
async def rase_exception() -> NoReturn:
    raise ValueError("This thing is just always failing!")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        logger.critical("YOU GOTTA SEE THIS LOG!")

        return await call_next(request)


## This line is the problematic one
app.add_middleware(LoggingMiddleware)


def default_error_handler(request: Request, exception: Exception):
    data = {
        'error': 'HandledError',
        'error_description': 'Unknown error obtained by the ServerErrorHandler'
    }
    return JSONResponse(data, status_code=getattr(exception, 'status_code', 500))


app.add_exception_handler(Exception, default_error_handler)


def _main():
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=2425,
        log_level='info'
    )


if __name__ == '__main__':
    _main()
