from kapita.core.data.dto.base import BaseDTO
from kapita.core.data.enum import UserRole


class AuthenticatedDTO(BaseDTO):
    """AuthenticatedDTO."""

    id: int

    username: str

    role: UserRole
    is_active: bool

    token: str | None

    ip: str
