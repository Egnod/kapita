import logging
import logging.handlers

import logfire

from kapita.__about__ import __project__, __version__
from kapita.config import settings

__all__ = ["set_logs"]


def set_logs() -> None:
    """set_logs.

    :rtype: None
    """

    handlers = []

    if settings.infra.logfire.token:
        logfire.configure(
            token=settings.infra.logfire.token,
            service_name=__project__,
            service_version=__version__,
            environment=settings.common.environment,
        )
        handlers.append(logfire.LogfireLoggingHandler())

    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.basicConfig(level=settings.logging.level, handlers=handlers)
