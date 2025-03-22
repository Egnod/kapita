from __future__ import annotations

import datetime
import typing

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from iso4217 import Currency

from kapita.core.data.models.base import BaseModel

if typing.TYPE_CHECKING:
    from kapita.core.data.models.user import UserModel


class PortfolioStockModel(BaseModel):
    """PortfolioStockModel."""

    __tablename__ = "portfolios_stocks"

    id: sa_orm.Mapped[int] = sa_orm.mapped_column(sa.BigInteger, primary_key=True, autoincrement=True, init=False)

    symbol: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(64), nullable=False)

    user_id: sa_orm.Mapped[int] = sa_orm.mapped_column(
        sa.BigInteger,
        sa.ForeignKey("users.id", ondelete="RESTRICT"),
    )
    user: sa_orm.Mapped[UserModel] = sa_orm.relationship("UserModel", init=False, lazy="noload", foreign_keys=[user_id])

    currency: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(3), nullable=False, default=Currency.USD.code)
    is_removed: sa_orm.Mapped[bool] = sa_orm.mapped_column(nullable=False, default=True, server_default=sa.true())

    created_at: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(),
        server_default=sa.func.now(),
        default_factory=lambda: datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        init=False,
    )
