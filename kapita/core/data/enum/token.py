from kapita.core.data.enum.base import BaseStrEnum


class TokenType(BaseStrEnum):
    registartion_verify = "registartion_verify"
    password_recovery = "password_recovery"  # nosec
    login = "login"
    refresh = "refresh"
