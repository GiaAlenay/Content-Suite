from abc import ABC, abstractmethod
from typing import Optional, List

from dddpy.manual_record.domain.manual_record_entity import ManualRecordEntity


class ManualRecordQueryRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[ManualRecordEntity]:
        pass

    @abstractmethod
    def get_by_manual_record_brand_id(
        self, manual_record_brand_id: str
    ) -> Optional[ManualRecordEntity]:
        pass

    @abstractmethod
    def list_all(self) -> List[ManualRecordEntity]:
        pass
