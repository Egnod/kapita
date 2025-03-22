import typing as t

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource

from kapita.config.parts import CommonSettings, InfraSettings, LoggingSettings


class AppSettings(BaseSettings):
    """Summary settings."""

    common: CommonSettings
    infra: InfraSettings
    logging: LoggingSettings

    model_config = SettingsConfigDict(toml_file="config.toml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: t.Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> t.Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


settings = AppSettings()


__all__ = [
    "AppSettings",
    "settings",
]
