from abc import ABC, abstractmethod
from typing import Optional
from dddpy.brand.domain.brand_entity import BrandEntity
from dddpy.brand.domain.brand_data import CreateBrandData, UpdateBrandData


class BrandCmdRepository(ABC):

    @abstractmethod
    def create(self, brand: CreateBrandData) -> BrandEntity:
        pass

    @abstractmethod
    def update(self, id: int, brand: UpdateBrandData) -> Optional[BrandEntity]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
