import typing

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql

from kapita.core.data.cache.encoder import CacheEncoder
from kapita.core.data.cache.keys import CacheExpire, CacheKeys
from kapita.core.data.dao.base import BaseDAO
from kapita.core.data.models.cache import CacheModel


class CacheStore(BaseDAO[CacheModel]):
    """CacheStore."""

    _model = CacheModel

    async def clean(self) -> None:
        await self.delete_many(
            (self._model.created_at + sa.func.cast(sa.func.concat(self._model.ttl, " SECONDS"), sa.Interval))
            < sa.func.now()
        )

    async def get(self, key: CacheKeys, **key_parts: typing.Any) -> typing.Any | None:
        cache = await self.filter_one(self._model.key == key.value.format(**key_parts))

        if not cache or cache.is_expired:
            return None

        return CacheEncoder.loads(cache.value)

    async def set(self, key: CacheKeys, value: typing.Any, ttl: int | None = None, **key_parts: typing.Any) -> None:
        if not ttl:
            ttl = getattr(CacheExpire, key.name)

        statement = psql.insert(CacheModel).values(
            key=key.value.format(**key_parts), value=CacheEncoder.dumps(value), ttl=ttl
        )
        statement = statement.on_conflict_do_update(
            index_elements=["key"],
            set_={"key": key.value.format(**key_parts), "value": CacheEncoder.dumps(value), "ttl": ttl},
        )

        await self.session.execute(statement)

    async def remove(self, key: CacheKeys, **key_parts: dict[str, str | int]) -> None:
        await self.delete(self._model.key == key.value.format(**key_parts))
