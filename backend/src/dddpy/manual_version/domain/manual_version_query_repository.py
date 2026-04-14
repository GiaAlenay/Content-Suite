from abc import ABC, abstractmethod
from typing import Optional, List

from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity


class ManualVersionQueryRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[ManualVersionEntity]:
        pass

    @abstractmethod
    def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ManualVersionEntity]:
        pass

    @abstractmethod
    def get_by_manual_version_brand_id(
        self, manual_version_brand_id: str
    ) -> List[ManualVersionEntity]:
        pass

    @abstractmethod
    def list_all(self) -> List[ManualVersionEntity]:
        pass
