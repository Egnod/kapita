import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncEngine

from kapita.core.data.engine import create_sessionmaker

logger = logging.getLogger(__name__)


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, engine: AsyncEngine, pass_name: str = "session") -> None:  # nosec
        self.engine = engine
        self.sessionmaker = create_sessionmaker(engine)
        self.pass_name = pass_name

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.sessionmaker() as session:
            try:
                data[self.pass_name] = session

                result = await handler(event, data)
                await session.commit()
            except BaseException:
                logger.exception("Error on session work!", exc_info=True, stack_info=True)
                await session.rollback()
                raise

        return result
