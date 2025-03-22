import logging

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from kapita.bot.filters.chat import ChatTypeFilter
from kapita.core.data.models import UserModel

router = Router()
logger = logging.getLogger(__name__)


@router.message(ChatTypeFilter(["private"]), Command("start"))
async def get_user(
    message: Message,
    user: UserModel,
) -> None:
    await message.answer(
        f"Hello, @{user.username}!\n\nI'm a bot that can help you with Portfolio.",
        parse_mode=ParseMode.HTML,
    )
