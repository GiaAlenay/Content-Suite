from dddpy.manual_section.usecase.manual_section_cmd_schema import (
    CreateManualSectionSchema,
)
from dddpy.manual_section.domain.manual_section_data import (
    CreateManualSectionData,
)

from dddpy.manual_section.domain.manual_section_cmd_repository import (
    ManualSectionCmdRepository,
)
from dddpy.manual_section.domain.manual_section_entity import ManualSectionEntity
from dddpy.shared.logging.logging import Logger
from typing import List

logging = Logger("ManualSectionCmdUseCase")


class ManualSectionCmdUseCase:

    def __init__(self, repository: ManualSectionCmdRepository):
        self.repository = repository
        logging.info("ManualSectionCmdUseCase initialized")

    async def create(self, manual_section_data: CreateManualSectionSchema):
        logging.info(
            f"Delegating manual_section creation for manual_version_id={manual_section_data.manual_version_id}"
        )
        data = CreateManualSectionData(
            manual_version_id=manual_section_data.manual_version_id,
            section_name=manual_section_data.section_name,
            content=manual_section_data.content,
            order_number=manual_section_data.order_number,
        )

        return await self.repository.create(data)

    async def bulk_insert(
        self, manual_section_list: list[CreateManualSectionSchema]
    ) -> List[ManualSectionEntity]:
        logging.info(f"Delegating creation list for ")
        data_list = [
            CreateManualSectionData(
                manual_version_id=bmv.manual_version_id,
                section_name=bmv.section_name,
                content=bmv.content,
                order_number=bmv.order_number,
            )
            for bmv in manual_section_list
        ]
        return await self.repository.bulk_insert(data_list)
