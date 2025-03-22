from kapita.core.data.dao.base import BaseDAO
from kapita.core.data.models import PortfolioModel


class PortfolioDAO(BaseDAO[PortfolioModel]):
    """PortfolioDAO."""

    _model = PortfolioModel
