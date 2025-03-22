import logging

from aiogram import F, Router, md
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from kapita.bot.filters.chat import ChatTypeFilter
from kapita.bot.filters.portfolio import (
    PortfolioCreateCallback,
    PortfolioCreateCurrencyChooseCallback,
    PortfolioDeleteCallback,
    PortfolioInfoCallback,
    PortfolioSwitchToListCallback,
)
from kapita.bot.states.portfolio import PortfolioCreateState
from kapita.core.data.dao.portfolio import PortfolioDAO
from kapita.core.data.models import UserModel
from kapita.core.data.models.portfolio import PortfolioModel
from kapita.core.data.utils.currency import ALLOWED_CURRENCIES

router = Router()
logger = logging.getLogger(__name__)


async def get_portfolios_list(session: AsyncSession, user: UserModel) -> tuple[str, InlineKeyboardMarkup]:
    user_portfolios = await PortfolioDAO(session).filter_many(
        PortfolioModel.user_id == user.id, PortfolioModel.is_active.is_(True)
    )

    builder = InlineKeyboardBuilder()

    for portfolio in user_portfolios:
        builder.row(
            InlineKeyboardButton(
                text=f"{portfolio.title} — {portfolio.currency}",
                callback_data=PortfolioInfoCallback(id=portfolio.id).pack(),
            )
        )

    if len(user_portfolios) < 3:
        builder.row(InlineKeyboardButton(text="Create portfolio", callback_data=PortfolioCreateCallback().pack()))

    if not user_portfolios:
        message_text = "You don't have any portfolios yet."
    else:
        message_text = "Your portfolios"

    return message_text, builder.as_markup()


@router.message(ChatTypeFilter(["private"]), Command("portfolios"))
async def get_portfolio(
    message: Message,
    session: AsyncSession,
    user: UserModel,
) -> None:
    message_text, kb = await get_portfolios_list(session, user)

    await message.answer(md.italic(message_text), parse_mode=ParseMode.MARKDOWN, reply_markup=kb)


@router.callback_query(PortfolioInfoCallback.filter())
async def info_portfolio(
    callback: CallbackQuery,
    callback_data: PortfolioInfoCallback,
    session: AsyncSession,
) -> None:
    portfolio = await PortfolioDAO(session).filter_one(
        PortfolioModel.id == callback_data.id, PortfolioModel.is_active.is_(True)
    )

    if not portfolio:
        await callback.message.edit_text(
            md.italic("Portfolio not found, maybe you delete it"), parse_mode=ParseMode.MARKDOWN
        )
        return

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Delete", callback_data=PortfolioDeleteCallback(id=portfolio.id).pack()))
    builder.row(InlineKeyboardButton(text="Back to list", callback_data=PortfolioSwitchToListCallback().pack()))

    await callback.message.edit_text(
        f"Title: {md.italic(portfolio.title)}\nCurrency: {md.bold(portfolio.currency)}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=builder.as_markup(),
    )


@router.callback_query(PortfolioSwitchToListCallback.filter())
async def to_list_portfolio(
    callback: CallbackQuery,
    session: AsyncSession,
    user: UserModel,
) -> None:
    message_text, kb = await get_portfolios_list(session, user)

    await callback.message.edit_text(
        message_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb,
    )


@router.callback_query(PortfolioDeleteCallback.filter())
async def delete_portfolio(
    callback: CallbackQuery,
    callback_data: PortfolioInfoCallback,
    session: AsyncSession,
    user: UserModel,
) -> None:
    portfolio = await PortfolioDAO(session).filter_one(
        PortfolioModel.id == callback_data.id, PortfolioModel.is_active.is_(True)
    )

    if not portfolio:
        await callback.message.edit_text(
            md.italic("Portfolio not found, maybe you delete it"), parse_mode=ParseMode.MARKDOWN
        )
        return

    await PortfolioDAO(session).update_by_id(callback_data.id, is_active=False)

    _, kb = await get_portfolios_list(session, user)

    await callback.message.edit_text(
        f"Portfolio {md.italic(portfolio.title)} deleted", parse_mode=ParseMode.MARKDOWN, reply_markup=kb
    )


@router.callback_query(PortfolioCreateCallback.filter())
async def create_portfolio(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.edit_text(md.italic("Please, input title for new portfolio"), parse_mode=ParseMode.MARKDOWN)

    await state.set_state(PortfolioCreateState.title_input)


@router.message(F.text, PortfolioCreateState.title_input)
async def create_portfolio_input_title(
    message: Message,
    state: FSMContext,
) -> None:
    if len(message.text) > 64:
        await message.reply(md.italic("Portfolio title too long (max length - 64)"), parse_mode=ParseMode.MARKDOWN)
        return

    builder = InlineKeyboardBuilder()

    for currency in [c.code.upper() for c in ALLOWED_CURRENCIES]:
        builder.row(
            InlineKeyboardButton(
                text=currency, callback_data=PortfolioCreateCurrencyChooseCallback(currency=currency).pack()
            )
        )

    await message.reply(
        md.italic("Please, choose currency for new portfolio."),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=builder.as_markup(),
    )
    await state.update_data(title=message.text)
    await state.set_state(PortfolioCreateState.currency_input)


@router.callback_query(PortfolioCreateCurrencyChooseCallback.filter(), PortfolioCreateState.currency_input)
async def create_portfolio_input_currency(
    callback: CallbackQuery,
    callback_data: PortfolioCreateCurrencyChooseCallback,
    session: AsyncSession,
    user: UserModel,
    state: FSMContext,
) -> None:
    title = await state.get_value("title")

    await PortfolioDAO(session).create(user_id=user.id, title=title, description="", currency=callback_data.currency)

    _, kb = await get_portfolios_list(session, user)

    await callback.message.edit_text(md.italic("Portfolio created"), parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    await state.clear()
