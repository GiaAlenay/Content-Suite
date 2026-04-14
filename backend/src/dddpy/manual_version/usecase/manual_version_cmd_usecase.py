from dddpy.manual_version.usecase.manual_version_cmd_schema import (
    CreateManualVersionSchema,
    UpdateManualVersionSchema,
)
from dddpy.manual_version.domain.manual_version_data import (
    CreateManualVersionData,
    UpdateManualVersionData,
)

from dddpy.manual_version.domain.manual_version_cmd_repository import (
    ManualVersionCmdRepository,
)
from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity

from typing import Optional
from dddpy.shared.logging.logging import Logger

logging = Logger("ManualVersionCmdUseCase")


class ManualVersionCmdUseCase:

    def __init__(self, repository: ManualVersionCmdRepository):
        self.repository = repository
        logging.info("ManualVersionCmdUseCase initialized")

    async def create(self, manual_version_data: CreateManualVersionSchema):
        logging.info(
            f"Delegating manual_version creation for brand_id={manual_version_data.brand_id}"
        )
        data = CreateManualVersionData(
            brand_id=manual_version_data.brand_id,
            version_number=manual_version_data.version_number,
            full_content=manual_version_data.full_content,
            raw_parameters=manual_version_data.raw_parameters,
            status=manual_version_data.status,
            url_pdf_manual=manual_version_data.url_pdf_manual,
        )

        return await self.repository.create(data)

    async def update(
        self, id: str, manual_version_data: UpdateManualVersionSchema
    ) -> Optional[ManualVersionEntity]:
        logging.info(f"Delegating manual_version update for id={id}")
        data = UpdateManualVersionData(
            status=manual_version_data.status,
            url_pdf_manual=manual_version_data.url_pdf_manual,
        )
        return await self.repository.update(id, data)
