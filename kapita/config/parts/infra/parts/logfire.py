from pydantic import Field

from kapita.config.parts.base import BaseSettingsModel


class LogfireSettings(BaseSettingsModel):
    """LogfireSettings."""

    token: str | None = Field(default=None)
