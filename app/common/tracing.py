import contextvars

from fastapi import FastAPI, Request
from logging import getLogger
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import config

logger = getLogger(__name__)

ctx_trace_id = contextvars.ContextVar('trace_id')
ctx_request = contextvars.ContextVar('request')
ctx_response = contextvars.ContextVar('response')

# Populates context variables making them accessible for the
# duration of the request.
class TraceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_trace_id = request.headers.get(config.tracing_header, None)
        if req_trace_id:
            ctx_trace_id.set(req_trace_id)

        ctx_request.set({
            "url": str(request.url),
            "method": request.method
        })

        response = await call_next(request)

        ctx_response.set({"status_code": response.status_code})
        return response
