from dddpy.manual_section.usecase.manual_section_cmd_usecase import (
    ManualSectionCmdUseCase,
)
from dddpy.manual_section.usecase.manual_section_query_usecase import (
    ManualSectionQueryUseCase,
)
from dddpy.manual_section.usecase.manual_section_factory import (
    manual_section_cmd_usecase_factory,
    manual_section_query_usecase_factory,
)
from dddpy.manual_section.usecase.manual_section_cmd_schema import (
    CreateManualSectionSchema,
    UpdateManualSectionSchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("manual_section_usecase")

from dddpy.manual_section.domain.manual_section_exception import ManualSectionNotFound
from dddpy.manual_section.domain.manual_section_success import (
    ManualSectionSucessMessage,
)


class ManualSectionUseCase:
    def __init__(self):
        logging.info("__init__")
        self.manual_section_cmd_usecase: ManualSectionCmdUseCase = (
            manual_section_cmd_usecase_factory()
        )
        self.manual_section_query_usecase: ManualSectionQueryUseCase = (
            manual_section_query_usecase_factory()
        )
        logging.info("ManualSectionUseCase initialized")

    async def create(self, manual_section_data: CreateManualSectionSchema):
        logging.info("create")
        logging.info(f"Creating a new manual_section with data: {manual_section_data}")

        new_manual_section = await self.manual_section_cmd_usecase.create(
            manual_section_data
        )
        success = ResponseSuccessSchema(
            success=True,
            message=ManualSectionSucessMessage.MANUALRECORD_CREATED,
            data=new_manual_section.to_dict(),
        )
        logging.info(f"ManualSection created successfully: {success}")
        return success

    async def get_by_id(self, id: str):
        logging.info("get_by_id")
        manual_section = await self.manual_section_query_usecase.get_by_id(id)
        if not manual_section:
            raise ManualSectionNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ManualSectionSucessMessage.MANUALRECORD_GET,
            data=manual_section.to_dict(),
        )
        logging.info(f"ManualSection retrieved successfully by id={id}")
        return success

    async def get_by_manual_section_brand_id(self, manual_section_brand_id: str):
        logging.info("get_by_manual_section_brand_id")
        manual_section = (
            self.manual_section_query_usecase.get_by_manual_section_brand_id(
                manual_section_brand_id
            )
        )

        success = ResponseSuccessSchema(
            success=True,
            message=ManualSectionSucessMessage.MANUALRECORD_GET,
            data=manual_section.to_dict(),
        )
        logging.info(
            f"ManualSection retrieved successfully by brand_id={manual_section_brand_id}"
        )
        return success

    async def update(self, id: str, manual_section_data: UpdateManualSectionSchema):
        logging.info("update")
        logging.info(f"Updating manual_section {id} with data: {manual_section_data}")

        updated_manual_section = await self.manual_section_cmd_usecase.update(
            id, manual_section_data
        )
        if not updated_manual_section:
            raise ManualSectionNotFound()

        success = ResponseSuccessSchema(
            success=True,
            message=ManualSectionSucessMessage.MANUALRECORD_UPDATED,
            data=updated_manual_section.to_dict(),
        )
        logging.info(f"ManualSection updated successfully: {success}")
        return success

    async def list_all(self):
        logging.info("list_all")
        manual_section = await self.manual_section_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=ManualSectionSucessMessage.MANUALRECORDS_GET,
            data=[c.to_dict() for c in manual_section],
        )
        logging.info(
            f"ManualSections listed successfully: {len(manual_section)} manual_section"
        )
        return success
