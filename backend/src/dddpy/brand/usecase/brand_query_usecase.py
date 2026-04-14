from dddpy.brand.domain.brand_query_repository import BrandQueryRepository
from dddpy.brand.domain.brand_entity import BrandEntity

from typing import Optional, List


from dddpy.shared.logging.logging import Logger

logging = Logger("BrandQueryUseCase")


class BrandQueryUseCase:

    def __init__(self, repository: BrandQueryRepository):
        logging.info("BrandQueryUseCase initialized")
        self.repository = repository

    async def get_by_id(self, id: str) -> Optional[BrandEntity]:
        logging.info(f"Delegating brand fetch by id={id}")
        return await self.repository.get_by_id(id)

    async def get_by_code(self, code: str) -> Optional[BrandEntity]:
        logging.info(f"Delegating brand fetch by code={code}")
        return await self.repository.get_by_code(code)

    async def get_by_brand_name(self, brand_name: str) -> Optional[BrandEntity]:
        logging.info(f"Delegating brand fetch by name={brand_name}")
        return await self.repository.get_by_brand_name(brand_name)

    async def list_all(self) -> List[BrandEntity]:
        logging.info("Delegating brand list_all")
        return await self.repository.list_all()

    async def list_active_with_current_manual(self) -> List[BrandEntity]:
        logging.info("Delegating brand list_active_with_current_manual")
        return await self.repository.list_active_with_current_manual()
