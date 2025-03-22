import datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncEngine

from kapita.bot.tasks.base import BaseTask
from kapita.config import settings


def get_scheduler(engine: AsyncEngine) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(
        jobstores={"default": SQLAlchemyJobStore(url=settings.infra.database.uri)},
        timezone=datetime.UTC,
    )

    for task in BaseTask.get_tasks():
        scheduler.add_job(
            task.start,
            task.get_cron(),
            replace_existing=True,
            id=task.__name__,
            start_date=datetime.datetime.now(datetime.UTC),
        )

    return scheduler
