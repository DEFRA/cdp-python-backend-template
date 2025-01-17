import httpx


def async_client():
    client = httpx.AsyncClient()
    return client
