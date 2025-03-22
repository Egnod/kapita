from kapita.core.data.dao.base import BaseDAO
from kapita.core.data.models.user import UserModel


class UserDAO(BaseDAO[UserModel]):
    """UserDAO."""

    _model = UserModel
