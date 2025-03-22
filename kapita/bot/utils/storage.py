from copy import copy
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    StateType,
    StorageKey,
)
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from kapita.core.data.cache.keys import CacheKeys
from kapita.core.data.dao.cache import CacheStore


@dataclass
class MemoryStorageRecord:
    data: Dict[str, Any] = field(default_factory=dict)
    state: Optional[str] = None


class SQLAlchemyStorage(BaseStorage):
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.sessionmaker = async_sessionmaker(engine)

    async def close(self) -> None:
        pass

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        async with self.sessionmaker() as session:
            await CacheStore(session).set(
                CacheKeys.storage_state, state.state if isinstance(state, State) else state, **asdict(key)
            )

    async def get_state(self, key: StorageKey) -> Optional[str]:
        async with self.sessionmaker() as session:
            result = await CacheStore(session).get(CacheKeys.storage_state, **asdict(key))
        return result

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        async with self.sessionmaker() as session:
            await CacheStore(session).set(CacheKeys.storage_data, data.copy(), **asdict(key))

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        async with self.sessionmaker() as session:
            result = (await CacheStore(session).get(CacheKeys.storage_data, **asdict(key))) or {}
        return result

    async def get_value(self, storage_key: StorageKey, dict_key: str, default: Optional[Any] = None) -> Optional[Any]:
        data = await self.get_data(storage_key)
        return copy(data.get(dict_key, default))
