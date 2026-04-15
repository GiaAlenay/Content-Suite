from abc import ABC, abstractmethod
from typing import Optional, List
from dddpy.manual_section.domain.manual_section_entity import ManualSectionEntity
from dddpy.manual_section.domain.manual_section_data import (
    CreateManualSectionData,
    UpdateManualSectionData,
)


class ManualSectionCmdRepository(ABC):

    @abstractmethod
    async def create(
        self, manual_section: CreateManualSectionData
    ) -> ManualSectionEntity:
        pass

    @abstractmethod
    async def update(
        self, id: str, manual_section: UpdateManualSectionData
    ) -> Optional[ManualSectionEntity]:
        pass

    @abstractmethod
    async def bulk_insert(
        self, manual_section_list: list[CreateManualSectionData]
    ) -> List[ManualSectionEntity]:
        pass
