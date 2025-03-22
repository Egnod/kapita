from pydantic import Field

from kapita.config.parts.base import BaseSettingsModel


class CommonSettings(BaseSettingsModel):
    """CommonSettings."""

    environment: str = Field(...)

    def is_testnet(self) -> bool:
        """"""
        return not self.is_production()

    def is_production(self) -> bool:
        """is_production.

        Args:

        Returns:
            bool:
        """
        return self.environment == "production"

    def is_local(self) -> bool:
        """is_local.

        Args:

        Returns:
            bool:
        """
        return self.environment == "local"


__all__ = [
    "CommonSettings",
]
