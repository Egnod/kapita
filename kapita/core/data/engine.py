from sqlalchemy import Engine
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool, Pool

from kapita.config import settings

__all__ = ["create_engine"]


def create_engine(
    uri: str | None = None,
    poolclass: type[Pool] = AsyncAdaptedQueuePool,
    size: int = 8,
    is_async: bool = True,
    isolation_level: str | None = None,
) -> AsyncEngine | Engine:
    """Create sqla enigne for connection.

    Args:
      poolclass: type[Pool]:  (Default value = AsyncAdaptedQueuePool)
      size: int:  (Default value = 128)
      is_async: bool:  (Default value = True)

    Returns:
    """

    if not uri:
        uri = settings.infra.database.uri

    kwargs = {}

    if isolation_level:
        kwargs["isolation_level"] = isolation_level

    pool_kwargs = {}

    if poolclass in (AsyncAdaptedQueuePool,):
        pool_kwargs.update(
            {
                "pool_size": size,
                "max_overflow": 0,
                "pool_recycle": 1800,
                "pool_timeout": 10,
            }
        )

    if is_async:
        engine = create_async_engine(uri, echo=False, poolclass=poolclass, execution_options=kwargs, **pool_kwargs)
    else:
        engine = create_sync_engine(uri, echo=False, poolclass=poolclass, execution_options=kwargs, **pool_kwargs)

    return engine


def create_sessionmaker(engine: AsyncEngine | Engine) -> async_sessionmaker[AsyncSession] | sessionmaker[Session]:
    """

    Args:
      engine: AsyncEngine | Engine:

    Returns:

    """
    if isinstance(engine, AsyncEngine):
        return async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    elif isinstance(engine, Engine):
        return sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    else:
        raise TypeError(f"Engine type error! {engine.__class__}")
