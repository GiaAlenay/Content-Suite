from dddpy.manual_record.domain.manual_record_query_repository import (
    ManualRecordQueryRepository,
)
from dddpy.manual_record.domain.manual_record_entity import ManualRecordEntity

from typing import Optional, List


from dddpy.shared.logging.logging import Logger

logging = Logger("ManualRecordQueryUseCase")


class ManualRecordQueryUseCase:

    def __init__(self, repository: ManualRecordQueryRepository):
        logging.info("ManualRecordQueryUseCase initialized")
        self.repository = repository

    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ManualRecordEntity]:
        logging.info(
            f"Delegating manual_record fetch by brand_id={brand_id} latest version"
        )
        return await self.repository.get_current_version_by_brand_id(brand_id)

    async def get_by_id(self, id: str) -> Optional[ManualRecordEntity]:
        logging.info(f"Delegating manual_record fetch by id={id}")
        return await self.repository.get_by_id(id)

    async def get_by_manual_record_brand_id(
        self, manual_record_brand_id: str
    ) -> Optional[ManualRecordEntity]:
        logging.info(
            f"Delegating manual_record fetch by brand_id={manual_record_brand_id}"
        )
        return await self.repository.get_by_manual_record_brand_id(
            manual_record_brand_id
        )

    async def list_all(self) -> List[ManualRecordEntity]:
        logging.info("Delegating manual_record list_all")
        return await self.repository.list_all()
