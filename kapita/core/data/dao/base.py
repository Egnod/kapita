import math
from typing import Any, Generic, TypeVar

import sqlalchemy as sa
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from kapita.core.data.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseDAO(Generic[T]):
    """BaseDAO."""

    _model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        """__init__.

        Args:
            session (AsyncSession): session

        Returns:
            None:
        """
        self.session = session

    async def delete(self, obj: T) -> None:
        """delete.

        :rtype: T
        """
        await self.session.execute(sa.delete(self._model).where(self._model.id == obj.id))

    async def delete_many(
        self,
        *whereclause: Any,
    ) -> None:
        """delete_many.

        :rtype: T
        """
        await self.session.execute(sa.delete(self._model).where(*whereclause))

    async def exists(self, *whereclause: Any) -> bool:  # noqa
        """Checks if a row exists in the table.

        Args:
                whereclause: a list of conditions to check

        Returns:
                True if the row with clauses exists
        """
        statement = sa.exists().where(*whereclause).select()

        return (await self.session.execute(statement)).scalar()

    async def count(self, *whereclause: Any, joins: list[BaseModel] | None = None) -> int:
        """count.

        Args:
            whereclause (Any): whereclause
            joins (list[BaseModel] | None): joins

        Returns:
            int:
        """
        if joins is None:
            joins = []

        base_statement = sa.select(sa.func.count(sa.text("1")))

        for join in joins:
            base_statement.join(join)

        statement = base_statement.select_from(self._model).where(*whereclause)

        return (await self.session.execute(statement)).scalar()

    async def execute(self, statement: Any) -> Any:
        """execute.

        Args:
            statement (Any): statement

        Returns:
            Any:
        """
        return await self.session.execute(statement)

    async def get_frames_count(self, *whereclause: Any, per_frame: int = 1) -> int:
        """get_frames_count.

        Args:
            whereclause (Any): whereclause
            per_frame (int): per_frame

        Returns:
            int:
        """
        if per_frame <= 0:
            return 0

        return math.ceil(await self.count(*whereclause) / per_frame)

    async def update(self, obj: T, **kwargs: Any) -> T:
        """update.

        :rtype: T
        """
        for attr, value in kwargs.items():
            setattr(obj, attr, value)

        self.session.add(obj)

        return obj

    async def update_by_id(self, obj_id: int, **values: Any) -> None:
        """update_by_id.

        :rtype: int
        """
        query = sa.update(self._model.__table__).where(self._model.id == obj_id).values(values)
        await self.session.execute(query)

    async def bulk_update(self, *whereclause: Any, **values: Any) -> None:
        """update."""
        query = (
            sa.update(self._model.__table__)
            .where(*whereclause)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )

        (await self.session.execute(query))

    async def increment(self, obj: T | int, field: Any, amount: float | int) -> None:
        """increment."""
        query = (
            sa.update(self._model.__table__)
            .where(self._model.id == obj if isinstance(obj, int) else obj.id)
            .values({field: field + amount})
        )

        (await self.session.execute(query))

    async def create(self, autoflush: bool = True, **kwargs: Any) -> T:
        """create.

        :rtype: T
        """
        obj = self._model(**kwargs)

        self.session.add(obj)

        if autoflush:
            await self.session.flush([obj])

        return obj

    async def filter_by_user_id(self, user_id: str) -> list[T]:
        """filter_by_user_id.

        Args:
            user_id (str): user_id

        Returns:
            list[T]:
        """
        if not hasattr(self._model, "user_id"):
            raise RuntimeError(f"{self._model} hasn't user_id!")

        query = sa.select(self._model).where(self._model.user_id == user_id)

        return (await self.session.execute(query)).scalars().all()

    async def filter_many(  # noqa: CCR001
        self,
        *whereclause: Any,
        order_by: sa.UnaryExpression | tuple[sa.UnaryExpression, ...] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        distinct_by: sa.UnaryExpression | None = None,
    ) -> list[T]:
        """filter_many.

        Args:
            whereclause (Any): whereclause
            order_by (sa.UnaryExpression | None): order_by
            limit (int | None): limit
            offset (int | None): offset

        Returns:
            list[T]:
        """
        subquery = sa.select(self._model).where(*whereclause)

        if distinct_by is not None:
            subquery = subquery.distinct(distinct_by)

        if order_by is not None:
            if not isinstance(order_by, tuple) and not isinstance(order_by, list):
                order_by = (order_by,)

            subquery = subquery.subquery()
            query = sa.select(self._model).join(subquery, subquery.c.id == self._model.id).order_by(*order_by)
        else:
            query = subquery

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return (await self.session.execute(query)).scalars().all()

    async def filter_one(self, *whereclause: Any, for_update: bool = False) -> T | None:
        """filter_one.

        Args:
            whereclause (Any): whereclause

        Returns:
            T | None:
        """
        if not for_update:
            query = sa.select(self._model).where(*whereclause)
        else:
            query = sa.select(self._model).where(*whereclause).with_for_update()

        return (await self.session.execute(query)).scalar_one_or_none()

    async def get_by_id(self, id: int) -> T | None:
        """get_by_id.

        :param id:
        :type value: Any
        :rtype: T | None
        """

        return await self.filter_one(self._model.id == id)

    async def get_ids_by(self, **mapping: Any) -> T | None:
        """get_ids_by.

        Args:
            mapping (Any): mapping

        Returns:
            T | None:
        """
        ids = None

        obj_query = sa.select(self._model.id)

        for k, v in mapping.items():
            if not (field := getattr(self._model, k, None)):
                raise AttributeError(f"{self._model.__name__} doesn't have field {k}")

            if isinstance(v, list):
                obj_query = obj_query.where(or_(field == _v for _v in v))
            else:
                obj_query = obj_query.where(field == v)

        ids = (await self.session.scalars(obj_query)).all()

        return ids
