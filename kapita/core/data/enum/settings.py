from kapita.core.data.enum.base import BaseStrEnum


class SettingKey(BaseStrEnum):
    bot_session = "bot_session"
    bot_chat_id = "bot_chat_id"
    bot_restart_required = "bot_restart_required"
    is_watch_enabled = "is_watch_enabled"


SettingsType: dict[SettingKey, type] = {
    SettingKey.bot_session: str,
    SettingKey.bot_chat_id: str,
    SettingKey.is_watch_enabled: bool,
    SettingKey.bot_restart_required: bool,
}
