import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault

from kapita.bot.app import get_app
from kapita.bot.scheduler import get_scheduler
from kapita.config import settings
from kapita.core.data.engine import create_engine
from kapita.core.utils.logs import set_logs


async def main() -> None:
    engine = create_engine(uri=settings.infra.database.uri)
    autocommit_engine = create_engine(settings.infra.database.uri, isolation_level="AUTOCOMMIT")

    bot, dp = get_app(autocommit_engine, engine)
    scheduler = get_scheduler(engine)

    commands = [
        BotCommand(command="start", description="Welcome message"),
        BotCommand(command="portfolios", description="Manage your portfolios"),
        BotCommand(command="symbol", description="Search for symbols"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

    scheduler.start()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    scheduler.shutdown()


def start() -> None:
    set_logs()

    asyncio.run(main())


if __name__ == "__main__":
    start()
