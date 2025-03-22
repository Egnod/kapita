from __future__ import annotations

import logging
import typing
from abc import ABC, abstractmethod

import httpx
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession

from kapita.config.default import settings
from kapita.core.data.dao import CacheStore
from kapita.core.data.engine import create_engine

logger = logging.getLogger(__name__)


class BaseTask(ABC):
    crontab: str

    @classmethod
    def get_tasks(cls) -> list[type[BaseTask]]:
        return cls.__subclasses__()

    @classmethod
    async def start(cls) -> typing.Any | None:
        obj = cls()

        async with (
            AsyncSession(create_engine(settings.infra.database.uri, StaticPool)) as session,
            httpx.AsyncClient(timeout=httpx.Timeout(timeout=10, connect=15, read=15)) as http_client,
        ):
            try:
                results = await obj.run(session, CacheStore(session), http_client)
            except BaseException as e:
                logger.exception("Error on task %s working", obj.__class__.__name__, exc_info=e, stack_info=True)
                await session.rollback()

                raise e
            else:
                await session.commit()

        return results

    @classmethod
    def get_cron(cls) -> CronTrigger:
        return CronTrigger.from_crontab(cls.crontab)

    @abstractmethod
    async def run(
        self, session: AsyncSession, cache_store: CacheStore, http_client: httpx.AsyncClient
    ) -> typing.Any | None:
        pass
