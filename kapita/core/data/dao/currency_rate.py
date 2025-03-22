import datetime
import decimal

import sqlalchemy.dialects.postgresql as psql

from kapita.core.data.dao.base import BaseDAO
from kapita.core.data.models import CurrencyRateModel


class CurrencyRateDAO(BaseDAO[CurrencyRateModel]):
    """CurrencyRateDAO."""

    _model = CurrencyRateModel

    async def set(
        self, from_currency: str, to_currency: str, date: datetime.date, provider_identity: str, value: decimal.Decimal
    ) -> None:
        statement = psql.insert(CurrencyRateModel).values(
            from_currency=from_currency, to_currency=to_currency, date=date, value=value, provider=provider_identity
        )
        statement = statement.on_conflict_do_update(
            constraint="currency_rates_pkey",
            set_={"value": value},
        )

        await self.session.execute(statement)
