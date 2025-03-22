import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from kapita.core.data.dao.cache import CacheStore

logger = logging.getLogger(__name__)


class CacheStoreMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        cache_store = CacheStore(data["session"])

        data["cache_store"] = cache_store

        result = await handler(event, data)

        return result
