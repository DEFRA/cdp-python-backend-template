from typing import Optional

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict()
    host: Optional[str] = None
    port: Optional[int] = None
    log_config: Optional[str] = None
    mongo_uri: Optional[str] = None
    mongo_database: str = "cdp-python-backend-template"
    mongo_truststore: str = "TRUSTSTORE_CDP_ROOT_CA"
    aws_endpoint_url: Optional[str] = None
    http_proxy: Optional[HttpUrl] = None
    enable_metrics: bool = False
    tracing_header: str = "x-cdp-request-id"


config = AppConfig()
