import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from kapita.bot.tasks.base import BaseTask
from kapita.core.data.dao import CacheStore


class CleanOldCacheTask(BaseTask):
    crontab = "*/1 * * * *"

    async def run(self, session: AsyncSession, cache_store: CacheStore, http_client: httpx.AsyncClient) -> None:
        await cache_store.clean()
