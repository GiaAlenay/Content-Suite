from abc import ABC, abstractmethod
from typing import Optional
from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity
from dddpy.manual_version.domain.manual_version_data import (
    CreateManualVersionData,
    UpdateManualVersionData,
)


class ManualVersionCmdRepository(ABC):

    @abstractmethod
    def create(self, manual_version: CreateManualVersionData) -> ManualVersionEntity:
        pass

    @abstractmethod
    def update(
        self, id: str, manual_version: UpdateManualVersionData
    ) -> Optional[ManualVersionEntity]:
        pass
