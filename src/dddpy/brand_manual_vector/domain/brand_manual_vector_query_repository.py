from abc import ABC, abstractmethod
from typing import Optional, List
from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)


class BrandManualVectorQueryRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[BrandManualVectorEntity]:
        pass

    @abstractmethod
    def get_by_brand_id(self, brand_id: str) -> List[BrandManualVectorEntity]:
        pass

    @abstractmethod
    def list_all(self) -> List[BrandManualVectorEntity]:
        pass
