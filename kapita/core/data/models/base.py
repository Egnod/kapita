from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

__all__ = ["BaseModel"]


class BaseModel(MappedAsDataclass, DeclarativeBase):
    """BaseModel."""

    @classmethod
    def lookup(cls) -> list[type[BaseModel]]:
        """lookup.

        :rtype: list[type[T]]
        """
        return list(cls.__subclasses__())
