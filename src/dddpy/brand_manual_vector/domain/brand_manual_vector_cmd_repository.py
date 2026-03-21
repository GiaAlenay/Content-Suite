from abc import ABC, abstractmethod
from typing import Optional
from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_data import (
    CreateBrandManualVectorData,
    UpdateBrandManualVectorData,
)


class BrandManualVectorCmdRepository(ABC):

    @abstractmethod
    def create(
        self, brand_manual_vector: CreateBrandManualVectorData
    ) -> BrandManualVectorEntity:
        pass

    @abstractmethod
    def update(
        self, id: str, brand_manual_vector: UpdateBrandManualVectorData
    ) -> Optional[BrandManualVectorEntity]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
