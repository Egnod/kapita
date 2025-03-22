import datetime

import httpx
from iso4217 import Currency
from sqlalchemy.ext.asyncio import AsyncSession

from kapita.bot.tasks.base import BaseTask
from kapita.core.currency_rate import CurrencyRateClient
from kapita.core.data.dao import CacheStore, CurrencyRateDAO


class RefreshCurrencyRateTask(BaseTask):
    crontab = "*/1 * * * *"
    PAIRS = (
        (Currency.USD, Currency.EUR),
        (Currency.USD, Currency.RUB),
        (Currency.USD, Currency.CNY),
        (Currency.USD, Currency.JPY),
    )

    async def run(
        self, session: AsyncSession, cache_store: CacheStore, http_client: httpx.AsyncClient, date: datetime.date = None
    ) -> None:
        provider = CurrencyRateClient.get_default()(http_client)

        if not date:
            date = datetime.datetime.now(datetime.UTC).date()

        for pair in self.PAIRS:
            rate = await provider.get_rate(*pair, target_date=date)

            await CurrencyRateDAO(session).set(pair[0], pair[1], date, provider.identity, rate)
