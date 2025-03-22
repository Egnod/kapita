from kapita.core.data.enum.base import BaseStrEnum


class UserRole(BaseStrEnum):
    manager = "manager"
    admin = "admin"


class UserAddressType(BaseStrEnum):
    trc20 = "trc20"
