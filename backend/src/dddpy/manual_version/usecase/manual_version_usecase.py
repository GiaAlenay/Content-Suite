from dddpy.manual_version.usecase.manual_version_cmd_usecase import (
    ManualVersionCmdUseCase,
)
from dddpy.manual_version.usecase.manual_version_query_usecase import (
    ManualVersionQueryUseCase,
)
from dddpy.manual_version.usecase.manual_version_factory import (
    manual_version_cmd_usecase_factory,
    manual_version_query_usecase_factory,
)
from dddpy.manual_version.usecase.manual_version_cmd_schema import (
    CreateManualVersionSchema,
    UpdateManualVersionSchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("manual_version_usecase")

from dddpy.manual_version.domain.manual_version_exception import ManualVersionNotFound
from dddpy.manual_version.domain.manual_version_success import (
    ManualVersionSucessMessage,
)


class ManualVersionUseCase:
    def __init__(self):
        logging.info("__init__")
        self.manual_version_cmd_usecase: ManualVersionCmdUseCase = (
            manual_version_cmd_usecase_factory()
        )
        self.manual_version_query_usecase: ManualVersionQueryUseCase = (
            manual_version_query_usecase_factory()
        )
        logging.info("ManualVersionUseCase initialized")

    def create(self, manual_version_data: CreateManualVersionSchema):
        logging.info("create")
        logging.info(f"Creating a new manual_version with data: {manual_version_data}")

        new_manual_version = self.manual_version_cmd_usecase.create(manual_version_data)
        success = ResponseSuccessSchema(
            success=True,
            message=ManualVersionSucessMessage.ManualVersion_CREATED,
            data=new_manual_version.to_dict(),
        )
        logging.info(f"ManualVersion created successfully: {success}")
        return success

    def get_by_id(self, id: str):
        logging.info("get_by_id")
        manual_version = self.manual_version_query_usecase.get_by_id(id)
        if not manual_version:
            raise ManualVersionNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ManualVersionSucessMessage.ManualVersion_GET,
            data=manual_version.to_dict(),
        )
        logging.info(f"ManualVersion retrieved successfully by id={id}")
        return success

    def get_by_manual_version_brand_id(self, manual_version_brand_id: str):
        logging.info("get_by_manual_version_brand_id")
        manual_version = (
            self.manual_version_query_usecase.get_by_manual_version_brand_id(
                manual_version_brand_id
            )
        )

        success = ResponseSuccessSchema(
            success=True,
            message=ManualVersionSucessMessage.ManualVersion_GET,
            data=manual_version.to_dict(),
        )
        logging.info(
            f"ManualVersion retrieved successfully by brand_id={manual_version_brand_id}"
        )
        return success

    def update(self, id: str, manual_version_data: UpdateManualVersionSchema):
        logging.info("update")
        logging.info(f"Updating manual_version {id} with data: {manual_version_data}")

        updated_manual_version = self.manual_version_cmd_usecase.update(
            id, manual_version_data
        )
        if not updated_manual_version:
            raise ManualVersionNotFound()

        success = ResponseSuccessSchema(
            success=True,
            message=ManualVersionSucessMessage.ManualVersion_UPDATED,
            data=updated_manual_version.to_dict(),
        )
        logging.info(f"ManualVersion updated successfully: {success}")
        return success

    def list_all(self):
        logging.info("list_all")
        manual_version = self.manual_version_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=ManualVersionSucessMessage.ManualVersionS_GET,
            data=[c.to_dict() for c in manual_version],
        )
        logging.info(
            f"ManualVersions listed successfully: {len(manual_version)} manual_version"
        )
        return success
