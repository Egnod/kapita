from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncEngine

from kapita.bot.middlewares import CacheStoreMiddleware, DBSessionMiddleware, HTTPClientMiddleware, UserMiddleware
from kapita.bot.routers import portfolios_list, start
from kapita.bot.utils.storage import SQLAlchemyStorage
from kapita.config import settings


def get_app(
    autocommit_engine: AsyncEngine, engine: AsyncEngine, only_bot: bool = False
) -> tuple[Bot, Dispatcher | None]:
    bot = Bot(settings.infra.telegram.bot_token)

    if only_bot:
        return bot, None

    dp = Dispatcher(storage=SQLAlchemyStorage(autocommit_engine))

    dp.update.outer_middleware(
        DBSessionMiddleware(engine, pass_name="session")  # nosec
    )
    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(HTTPClientMiddleware())
    dp.update.outer_middleware(CacheStoreMiddleware())

    dp.include_routers(start.router)
    dp.include_routers(portfolios_list.router)

    return bot, dp
