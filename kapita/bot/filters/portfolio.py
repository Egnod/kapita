from aiogram.filters.callback_data import CallbackData


class PortfolioCreateCallback(CallbackData, prefix="portfolio_create"):
    pass


class PortfolioCreateCurrencyChooseCallback(CallbackData, prefix="portfolio_create_currency_choose"):
    currency: str


class PortfolioInfoCallback(CallbackData, prefix="portfolio_info"):
    id: int


class PortfolioDeleteCallback(CallbackData, prefix="portfolio_delete"):
    id: int


class PortfolioSwitchToListCallback(CallbackData, prefix="portfolio_switch_to_list"):
    pass
