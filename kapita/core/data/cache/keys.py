from kapita.core.data.enum.base import BaseStrEnum


class CacheKeys(BaseStrEnum):
    currency_rate = "_:{from_currency}:{to_currency}"
    storage_state = "__:{bot_id}:{chat_id}:{user_id}:{thread_id}:{business_connection_id}:{destiny}:s"
    storage_data = "__:{bot_id}:{chat_id}:{user_id}:{thread_id}:{business_connection_id}:{destiny}:d"


class CacheExpire:
    currency_rate = 60
    storage_data = storage_state = 60 * 60 * 6
