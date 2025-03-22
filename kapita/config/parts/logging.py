import logging

from pydantic import Field

from kapita.config.parts.base import BaseSettingsModel


class LoggingSettings(BaseSettingsModel):
    """LoggingSettings."""

    level: str = Field(default=logging.INFO)
