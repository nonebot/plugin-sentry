from typing import Any, Dict, List, Optional

from nonebot import get_driver
from sentry_sdk.integrations import Integration
from sentry_sdk.integrations.loguru import LoguruIntegration
from pydantic import Extra, Field, BaseModel, validator, root_validator

driver = get_driver()


class Config(BaseModel):
    sentry_dsn: Optional[str] = None
    sentry_environment: str = driver.env
    sentry_integrations: List[Integration] = Field(default_factory=list)

    # [FIXED] https://github.com/getsentry/sentry-python/issues/653
    # sentry_default_integrations: bool = False

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def filter_sentry_configs(cls, values: Dict[str, Any]):
        return {
            key: value for key, value in values.items() if key.startswith("sentry_")
        }

    @validator("sentry_integrations", allow_reuse=True, always=True)
    def validate_integrations(cls, v: List[Integration]):
        ids = {i.identifier for i in v}
        if LoguruIntegration.identifier not in ids:
            v.append(LoguruIntegration())
        return v
