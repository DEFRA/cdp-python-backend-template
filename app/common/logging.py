import logging
import ecs_logging

from app.common.tracing import ctx_trace_id, ctx_response, ctx_request

# Adds additional ECS fields to the logger.
class ExtraFieldsFilter(logging.Filter):
    def filter(self, record):
        trace_id = ctx_trace_id.get('')
        req = ctx_request.get(None)
        resp = ctx_response.get(None)

        if trace_id:
            record.trace = { "id": trace_id }

        print(req)
        http = {}
        if req:
            record.url = { "full": req.get('url') }
            http['request'] = {
                "method": req.get('method', None)
            }
        if resp:
            http['response'] = resp
        if http:
            record.http = http
        return True
