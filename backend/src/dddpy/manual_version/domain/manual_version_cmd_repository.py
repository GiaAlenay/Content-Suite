from abc import ABC, abstractmethod
from typing import Optional
from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity
from dddpy.manual_version.domain.manual_version_data import (
    CreateManualVersionData,
    UpdateManualVersionData,
)


class ManualVersionCmdRepository(ABC):

    @abstractmethod
    async def create(
        self, manual_version: CreateManualVersionData
    ) -> ManualVersionEntity:
        pass

    @abstractmethod
    async def update(
        self, id: str, manual_version: UpdateManualVersionData
    ) -> Optional[ManualVersionEntity]:
        pass
