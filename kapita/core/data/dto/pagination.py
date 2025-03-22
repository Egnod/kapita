from typing import Generic, TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

from kapita.core.data.dto.base import BaseDTO

T = TypeVar("T", bound=BaseDTO)


class PaginationRequestParams(BaseDTO):
    """PaginationRequestParams."""

    per_page: int = Field(default=10, gte=1)
    page: int = Field(default=1, gte=0)

    @property
    def skip(self) -> int:  # noqa: FNE002
        """skip.

        Args:

        Returns:
            int:
        """
        return self.per_page * (self.page - 1) if self.page > 0 else 0


class GenericField(GenericModel, Generic[T]):
    """GenericField."""

    data: list[T]


class PaginatedResponse(GenericField[T], Generic[T]):
    """PaginatedResponse."""

    pages_count: int = Field(default=0, gte=0)
    current_page: int = Field(default=0, gte=0)
    total: int = Field(default=0, gte=0)
