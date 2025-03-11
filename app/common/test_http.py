import httpx

from app.common.http import hook_request_tracing
from app.common.tracing import ctx_trace_id


def mockHandler(request):
    id = request.headers.get("x-cdp-request-id", "")
    return httpx.Response(200, text=id)


def test_trace_id_missing():
    ctx_trace_id.set("")
    client = httpx.Client(
        event_hooks={"request": [hook_request_tracing]},
        transport=httpx.MockTransport(mockHandler),
    )
    resp = client.get("http://localhost:1234/test")
    assert resp.text == ""


def test_trace_id_set():
    ctx_trace_id.set("trace-id-value")
    client = httpx.Client(
        event_hooks={"request": [hook_request_tracing]},
        transport=httpx.MockTransport(mockHandler),
    )
    resp = client.get("http://localhost:1234/test")
    assert resp.text == "trace-id-value"
