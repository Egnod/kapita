import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from kapita.core.data.dao.user import UserDAO

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        from_user = getattr(event, "from_user", None)

        if not from_user and (message := getattr(event, "message", None)):
            from_user = message.from_user
        elif not from_user and (message := getattr(event, "callback_query", None)):
            from_user = message.from_user

        user_dao = UserDAO(data["session"])
        user = await user_dao.get_by_id(from_user.id)

        if not user:
            user = await user_dao.create(
                id=from_user.id,
                username=from_user.username or "",
                first_name=from_user.first_name or "",
                last_name=from_user.last_name or "",
            )

        data["user"] = user

        result = await handler(event, data)

        return result
