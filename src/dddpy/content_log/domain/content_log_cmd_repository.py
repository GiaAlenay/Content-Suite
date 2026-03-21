from abc import ABC, abstractmethod
from typing import Optional
from dddpy.content_log.domain.content_log_entity import ContentLogEntity
from dddpy.content_log.domain.content_log_data import (
    CreateContentLogData,
    UpdateContentLogData,
)


class ContentLogCmdRepository(ABC):

    @abstractmethod
    def create(self, content_log: CreateContentLogData) -> ContentLogEntity:
        pass

    @abstractmethod
    def update(
        self, id: str, content_log: UpdateContentLogData
    ) -> Optional[ContentLogEntity]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
