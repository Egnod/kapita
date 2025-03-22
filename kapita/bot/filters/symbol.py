from aiogram.filters.callback_data import CallbackData


class SearchSymbolCallback(CallbackData, prefix="search_symbol"):
    query: str
    page: int
