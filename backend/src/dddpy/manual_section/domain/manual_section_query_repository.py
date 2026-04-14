from abc import ABC, abstractmethod
from typing import Optional, List

from dddpy.manual_section.domain.manual_section_entity import ManualSectionEntity


class ManualSectionQueryRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[ManualSectionEntity]:
        pass

    @abstractmethod
    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ManualSectionEntity]:
        pass

    @abstractmethod
    async def get_by_manual_section_brand_id(
        self, manual_section_brand_id: str
    ) -> List[ManualSectionEntity]:
        pass

    @abstractmethod
    async def list_all(self) -> List[ManualSectionEntity]:
        pass
