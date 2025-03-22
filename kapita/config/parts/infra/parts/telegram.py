from pydantic import Field

from kapita.config.parts.base import BaseSettingsModel


class TelegramSettings(BaseSettingsModel):
    """TelegramSettings."""

    api_id: int = Field(...)
    api_hash: str = Field(...)
    bot_token: str = Field(...)
