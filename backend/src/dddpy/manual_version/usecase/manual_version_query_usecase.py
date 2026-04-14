from dddpy.manual_version.domain.manual_version_query_repository import (
    ManualVersionQueryRepository,
)
from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity

from typing import Optional, List


from dddpy.shared.logging.logging import Logger

logging = Logger("ManualVersionQueryUseCase")


class ManualVersionQueryUseCase:

    def __init__(self, repository: ManualVersionQueryRepository):
        logging.info("ManualVersionQueryUseCase initialized")
        self.repository = repository

    def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ManualVersionEntity]:
        logging.info(
            f"Delegating manual_version fetch by brand_id={brand_id} latest version"
        )
        return self.repository.get_current_version_by_brand_id(brand_id)

    def get_by_id(self, id: str) -> Optional[ManualVersionEntity]:
        logging.info(f"Delegating manual_version fetch by id={id}")
        return self.repository.get_by_id(id)

    def get_by_manual_version_brand_id(
        self, manual_version_brand_id: str
    ) -> Optional[ManualVersionEntity]:
        logging.info(
            f"Delegating manual_version fetch by brand_id={manual_version_brand_id}"
        )
        return self.repository.get_by_manual_version_brand_id(manual_version_brand_id)

    def list_all(self) -> List[ManualVersionEntity]:
        logging.info("Delegating manual_version list_all")
        return self.repository.list_all()
