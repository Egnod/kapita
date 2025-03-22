from aiogram.filters.state import State, StatesGroup


class PortfolioCreateState(StatesGroup):
    title_input = State()
    currency_input = State()
