from pydantic import Field

from kapita.config.parts.base import BaseSettingsModel


class AlphaVantageSettings(BaseSettingsModel):
    """AlphaVantageSettings."""

    token: str = Field(...)
