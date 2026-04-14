from dddpy.brand_manual_vector.domain.brand_manual_vector_query_repository import (
    BrandManualVectorQueryRepository,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)

from typing import Optional, List


from dddpy.shared.logging.logging import Logger

logging = Logger("BrandManualVectorQueryUseCase")


class BrandManualVectorQueryUseCase:

    def __init__(self, repository: BrandManualVectorQueryRepository):
        logging.info("BrandManualVectorQueryUseCase initialized")
        self.repository = repository

    async def get_by_id(self, id: str) -> Optional[BrandManualVectorEntity]:
        logging.info(f"Delegating brand_manual_vector fetch by id={id}")
        return await self.repository.get_by_id(id)

    async def get_by_brand_id(self, brand_id: str) -> List[BrandManualVectorEntity]:
        logging.info(f"Delegating brand_manual_vector fetch by brand_id={brand_id}")
        return await self.repository.get_by_brand_id(brand_id)

    async def list_all(self) -> List[BrandManualVectorEntity]:
        logging.info("Delegating brand_manual_vector list_all")
        return await self.repository.list_all()

    async def search_brand_context(
        self, brand_id: str, vector: list[float], limit: int = 3
    ):
        logging.info(f"Buscando contexto vectorial para brand_id: {brand_id}")
        return await self.repository.search_brand_context(brand_id, vector, limit)
