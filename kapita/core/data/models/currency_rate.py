from __future__ import annotations

import datetime
import decimal

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from kapita.core.data.models.base import BaseModel


class CurrencyRateModel(BaseModel):
    """CurrencyRateModel."""

    __tablename__ = "currency_rates"

    from_currency: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(8), nullable=False, primary_key=True)
    to_currency: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(8), nullable=False, primary_key=True)
    provider: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(4), nullable=False, primary_key=True)
    date: sa_orm.Mapped[datetime.date] = sa_orm.mapped_column(sa.Date(), primary_key=True)

    value: sa_orm.Mapped[decimal.Decimal] = sa_orm.mapped_column(sa.Numeric(10, 2), nullable=False)
