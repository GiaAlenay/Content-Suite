from abc import ABC, abstractmethod
from typing import Optional, List
from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)


class BrandManualVectorQueryRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[BrandManualVectorEntity]:
        pass

    @abstractmethod
    async def get_by_brand_id(self, brand_id: str) -> List[BrandManualVectorEntity]:
        pass

    @abstractmethod
    async def list_all(self) -> List[BrandManualVectorEntity]:
        pass

    @abstractmethod
    async def search_brand_context(
        self, brand_id: str, vector: list[float], limit: int = 3
    ):
        pass
