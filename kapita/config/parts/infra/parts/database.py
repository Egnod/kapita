from pydantic import Field

from kapita.config.parts.base import BaseSettingsModel


class DBSettings(BaseSettingsModel):
    """DBSettings."""

    uri: str = Field(...)


__all__ = [
    "DBSettings",
]
