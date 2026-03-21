from abc import ABC, abstractmethod
from typing import Optional, List

from dddpy.brand.domain.brand_entity import BrandEntity


class BrandQueryRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[BrandEntity]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[BrandEntity]:
        pass

    @abstractmethod
    def get_by_brand_name(self, brand_name: str) -> Optional[BrandEntity]:
        pass

    @abstractmethod
    def list_all(self) -> List[BrandEntity]:
        pass
