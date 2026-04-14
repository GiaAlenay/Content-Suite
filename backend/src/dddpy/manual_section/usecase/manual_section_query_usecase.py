from dddpy.manual_section.domain.manual_section_query_repository import (
    ManualSectionQueryRepository,
)
from dddpy.manual_section.domain.manual_section_entity import ManualSectionEntity

from typing import Optional, List


from dddpy.shared.logging.logging import Logger

logging = Logger("ManualSectionQueryUseCase")


class ManualSectionQueryUseCase:

    def __init__(self, repository: ManualSectionQueryRepository):
        logging.info("ManualSectionQueryUseCase initialized")
        self.repository = repository

    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ManualSectionEntity]:
        logging.info(
            f"Delegating manual_section fetch by brand_id={brand_id} latest version"
        )
        return await self.repository.get_current_version_by_brand_id(brand_id)

    async def get_by_id(self, id: str) -> Optional[ManualSectionEntity]:
        logging.info(f"Delegating manual_section fetch by id={id}")
        return await self.repository.get_by_id(id)

    async def get_by_manual_section_brand_id(
        self, manual_section_brand_id: str
    ) -> Optional[ManualSectionEntity]:
        logging.info(
            f"Delegating manual_section fetch by brand_id={manual_section_brand_id}"
        )
        return await self.repository.get_by_manual_section_brand_id(
            manual_section_brand_id
        )

    async def list_all(self) -> List[ManualSectionEntity]:
        logging.info("Delegating manual_section list_all")
        return await self.repository.list_all()
