from __future__ import annotations

import datetime

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from kapita.core.data.models.base import BaseModel


class UserModel(BaseModel):
    """UserModel."""

    __tablename__ = "users"

    id: sa_orm.Mapped[int] = sa_orm.mapped_column(sa.BigInteger, primary_key=True)

    username: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(32), nullable=False)

    first_name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(16), nullable=False)
    last_name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(16), nullable=False)

    created_at: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(),
        server_default=sa.func.now(),
        default_factory=lambda: datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        init=False,
    )
