from pydantic import BaseModel

from kapita.config.parts.infra.parts import AlphaVantageSettings, DBSettings, LogfireSettings, TelegramSettings


class InfraSettings(BaseModel):
    """Summary settings."""

    database: DBSettings
    telegram: TelegramSettings
    logfire: LogfireSettings
    alphavantage: AlphaVantageSettings
