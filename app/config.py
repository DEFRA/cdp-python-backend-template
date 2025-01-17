from typing import Any, Callable, Set, Optional
from pydantic import (
    HttpUrl,
    MongoDsn
)
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict()
    port: int = 8085
    mongo_uri: str =  'mongodb://127.0.0.1:27017/'
    mongo_database: str = 'cdp-python-backend-template'
    http_proxy: Optional[HttpUrl] = None
    enable_metrics: bool = False
    tracing_header: str = 'x-cdp-request-id'

config = AppConfig()
