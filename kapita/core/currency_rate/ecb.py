import datetime
from decimal import Decimal
from typing import Dict

from defusedxml import ElementTree as ET
from iso4217 import Currency

from kapita.core.currency_rate.base import CurrencyRateClient


class ECBCurrencyRateClient(CurrencyRateClient):
    """
    Client for fetching currency rates from the European Bank of Russia (CBR) API.
    """

    base_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
    identity = "ECB"
    is_default = False

    MAX_PREVIOUS_DAYS = 7
    base_currency = Currency.EUR

    async def get_rate(
        self, from_currency: Currency, to_currency: Currency, target_date: datetime.date, current_previous_days: int = 0
    ) -> Decimal:
        """
        Fetch the currency rate for a specific date from the CBR API.

        :param from_currency: The currency code (e.g., Currency.usd for USD).
        :param to_currency: The currency code (e.g., Currency.usd for USD).
        :param target_date: The date for which the rate is requested.
        :return: The currency rate as a Decimal.
        """
        from_currency_pair_rate = None
        to_currency_pair_rate = None

        response = await self.http_client.get(self.base_url)

        response.raise_for_status()  # Проверка на ошибки HTTP

        # Безопасный парсинг XML с использованием defusedxml
        root = ET.fromstring(response.text)
        namespaces = {"gesmes": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}

        # Поиск курса для указанной даты
        for cube in root.findall(".//gesmes:Cube[@time]", namespaces=namespaces):
            if cube.attrib["time"] == target_date.isoformat():
                for rate in cube.findall("gesmes:Cube", namespaces=namespaces):
                    if rate.attrib["currency"] == from_currency.code:
                        from_currency_pair_rate = Decimal(1) / Decimal(rate.attrib["rate"])

                    if rate.attrib["currency"] == to_currency.code:
                        to_currency_pair_rate = Decimal(1) / Decimal(rate.attrib["rate"])

        if from_currency == self.base_currency:
            from_currency_pair_rate = Decimal(1)

        if to_currency == self.base_currency:
            to_currency_pair_rate = Decimal(1)

        if not from_currency_pair_rate or not to_currency_pair_rate:
            if current_previous_days >= self.MAX_PREVIOUS_DAYS:
                raise ValueError(f"Currency pair {from_currency.code}/{to_currency.code} not found")
            return await self.get_rate(
                from_currency,
                to_currency,
                target_date - datetime.timedelta(days=current_previous_days + 1),
                current_previous_days + 1,
            )
        else:
            return from_currency_pair_rate / to_currency_pair_rate

    async def get_rate_history(
        self, from_currency: Currency, to_currency: Currency, start_date: datetime.date, end_date: datetime.date
    ) -> Dict[datetime.date, Decimal]:
        """
        Fetch the currency rate history over a date range from the CBR API.

        :param from_currency: The currency code (e.g., Currency.usd for USD).
        :param to_currency: The currency code (e.g., Currency.usd for USD).
        :param start_date: The start date of the range.
        :param end_date: The end date of the range.
        :return: A dictionary where keys are dates and values are currency rates as Decimals.
        """
        history = {}
        current_date = start_date

        while current_date <= end_date:
            rate = await self.get_rate(from_currency, to_currency, current_date)

            history[current_date] = rate

            current_date += datetime.timedelta(days=1)

        return history
