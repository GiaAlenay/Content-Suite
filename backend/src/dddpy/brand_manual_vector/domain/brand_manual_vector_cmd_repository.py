from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_data import (
    CreateBrandManualVectorData,
    UpdateBrandManualVectorData,
)


class BrandManualVectorCmdRepository(ABC):

    @abstractmethod
    async def create(
        self, brand_manual_vector: CreateBrandManualVectorData
    ) -> Optional[BrandManualVectorEntity]:
        pass

    @abstractmethod
    async def update(
        self, id: str, brand_manual_vector: UpdateBrandManualVectorData
    ) -> Optional[BrandManualVectorEntity]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    async def deactivate_by_manual_version_id(
        self, manual_version_id: str
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def bulk_insert_vectors(self, vector_list: list[CreateBrandManualVectorData]):
        pass
