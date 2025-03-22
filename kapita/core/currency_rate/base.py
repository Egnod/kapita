from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal

import httpx
from iso4217 import Currency


class CurrencyRateClient(ABC):
    base_url: str
    identity: str
    is_default: bool

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        """
        Initialize the currency rate client with a base URL for the API.

        :param http_client: httpx.AsyncClient.
        """
        self.http_client = http_client

    @abstractmethod
    async def get_rate(self, from_currency: Currency, to_currency: Currency, target_date: date) -> Decimal:
        """
        Abstract method to fetch the currency rate for a specific date.

        :param from_currency: The currency code (e.g., "USD").
        :param to_currency: The currency code (e.g., "USD").
        :param target_date: The date for which the rate is requested.
        :return: The currency rate as a Decimal.
        """
        pass

    @abstractmethod
    async def get_rate_history(
        self, from_currency: Currency, to_currency: Currency, start_date: date, end_date: date
    ) -> dict[date, Decimal]:
        """
        Abstract method to fetch the currency rate history over a date range.

        :param from_currency: The currency code (e.g., "USD").
        :param to_currency: The currency code (e.g., "USD").
        :param start_date: The start date of the range.
        :param end_date: The end date of the range.
        :return: A dictionary where keys are dates and values are currency rates as Decimals.
        """
        pass

    @classmethod
    async def get_rate_by_identity(
        cls,
        http_client: httpx.AsyncClient,
        from_currency: Currency,
        to_currency: Currency,
        target_date: date,
        provider_identity: str | None = None,
    ) -> Decimal:
        """
        Get the currency rate for a specific date.

        :param from_currency: The currency code (e.g., "USD").
        :param to_currency: The currency code (e.g., "USD").
        :param target_date: The date for which the rate is requested.
        :param provider_identity: The provider of the currency rate.
        :return: The currency rate as a Decimal.
        """

        if provider_identity is None:
            provider_class = cls.get_default()
        else:
            provider_class = cls.get_by_identity(provider_identity)

        provider = provider_class(http_client)

        return await provider.get_rate(from_currency, to_currency, target_date)

    @classmethod
    async def get_rate_history_by_identity(
        cls,
        http_client: httpx.AsyncClient,
        from_currency: Currency,
        to_currency: Currency,
        start_date: date,
        end_date: date,
        provider_identity: str | None = None,
    ) -> dict[date, Decimal]:
        """
        Get the currency rate history over a date range.

        :param from_currency: The currency code (e.g., "USD").
        :param to_currency: The currency code (e.g., "USD").
        :param start_date: The start date of the range.
        :param end_date: The end date of the range.
        :param provider_identity: The provider of the currency rate.
        :return: A dictionary where keys are dates and values are currency rates as Decimals.
        """

        if provider_identity is None:
            provider_class = cls.get_default()
        else:
            provider_class = cls.get_by_identity(provider_identity)

        provider = provider_class(http_client)

        return await provider.get_rate_history(from_currency, to_currency, start_date, end_date)

    @classmethod
    def get_by_identity(cls, identity: str) -> type["CurrencyRateClient"] | None:
        """
        Get a currency rate client for a specific identity.

        :param identity: The identity of the currency rate client.
        :return: A currency rate client.
        """

        for client in cls.__subclasses__():
            if client.identity == identity:
                return client

        return None

    @classmethod
    def get_default(cls) -> type["CurrencyRateClient"] | None:
        """
        Get a currency rate default client.

        :return: A currency rate client.
        """

        for client in cls.__subclasses__():
            if client.is_default:
                return client

        return None
