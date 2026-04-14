from abc import ABC, abstractmethod
from typing import Optional
from dddpy.content_log.domain.content_log_entity import ContentLogEntity
from dddpy.content_log.domain.content_log_data import (
    CreateContentLogData,
    UpdateContentLogData,
)


class ContentLogCmdRepository(ABC):

    @abstractmethod
    async def create(
        self, content_log: CreateContentLogData
    ) -> Optional[ContentLogEntity]:
        pass

    @abstractmethod
    async def update(
        self, id: str, content_log: UpdateContentLogData
    ) -> Optional[ContentLogEntity]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass
