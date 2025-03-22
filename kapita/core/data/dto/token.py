import typing as t

from pydantic import Field

from kapita.core.data.dto.base import BaseDTO


class TokenDTO(BaseDTO):
    """TokenDTO."""

    type: str
    data: dict[str, t.Any] | None = Field(default=None)
