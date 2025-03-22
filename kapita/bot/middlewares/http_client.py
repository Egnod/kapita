import logging
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class HTTPClientMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.http_client = httpx.AsyncClient(timeout=httpx.Timeout(timeout=10, connect=15, read=15))

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["http_client"] = self.http_client

        result = await handler(event, data)

        return result
