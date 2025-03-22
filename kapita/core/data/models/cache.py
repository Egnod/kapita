from __future__ import annotations

import datetime
import typing as t

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from sqlalchemy.dialects import postgresql

from kapita.core.data.models.base import BaseModel


class CacheModel(BaseModel):
    """CacheModel."""

    __tablename__ = "cache"
    __table_args__ = {"prefixes": ["UNLOGGED"]}

    key: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String(255), nullable=False, primary_key=True)

    value: sa_orm.Mapped[t.Any] = sa_orm.mapped_column(
        postgresql.BYTEA, nullable=True, server_default=sa.null(), default=None
    )

    ttl: sa_orm.Mapped[int] = sa_orm.mapped_column(sa.Integer, nullable=False, default=0, server_default="0")
    created_at: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime,
        nullable=False,
        server_default=sa.func.now(),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )

    @property
    def is_expired(self) -> bool:
        if not self.ttl:
            return False

        return self.created_at + datetime.timedelta(seconds=self.ttl) < datetime.datetime.now()
