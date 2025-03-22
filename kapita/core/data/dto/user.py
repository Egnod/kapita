import datetime
from typing import Annotated

from pydantic import BeforeValidator, Field, SecretStr

from kapita.core.data.dto.base import BaseDTO
from kapita.core.data.enum import UserRole


def strip_n_lower(v: str) -> str:
    return v.strip().lower()


def check_password(value: str) -> SecretStr:
    if len(value) < 8:
        raise ValueError("Password must have at least 8 characters")

    if not any(c.isupper() for c in value):
        raise ValueError("Password must have at least one uppercase letter")

    if not any(c.islower() for c in value):
        raise ValueError("Password must have at least one lowercase letter")

    if not any(c.isdigit() for c in value):
        raise ValueError("Password must have at least one digit")

    return SecretStr(value)


UsernameApiType = Annotated[
    str,
    BeforeValidator(strip_n_lower),
]

PasswordType = Annotated[
    SecretStr,
    BeforeValidator(check_password),
]


class UserRegisterRequestDTO(BaseDTO):
    """UserRegisterRequestDTO."""

    username: UsernameApiType = Field(..., min_length=3, max_length=31)
    password: PasswordType = Field(..., min_length=3, max_length=31)
    role: UserRole = Field(default=UserRole.manager)


class UserResponseDTO(BaseDTO):
    """UserResponseDTO."""

    id: int

    username: UsernameApiType

    role: str

    is_active: bool

    created_at: datetime.datetime


class UserTokenDTO(BaseDTO):
    token: str
    refresh_token: str | None = Field(default=None)


class UserPasswordLoginDTO(BaseDTO):
    username: UsernameApiType
    password: SecretStr


class UserLoginRefreshDTO(BaseDTO):
    refresh_token: str


class UserChangePasswordDTO(BaseDTO):
    current_password: PasswordType
    new_password: PasswordType


class UserUpdateDTO(BaseDTO):
    username: UsernameApiType
    role: UserRole
    is_active: bool
