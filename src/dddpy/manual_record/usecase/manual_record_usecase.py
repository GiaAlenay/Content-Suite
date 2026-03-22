from dddpy.manual_record.usecase.manual_record_cmd_usecase import ManualRecordCmdUseCase
from dddpy.manual_record.usecase.manual_record_query_usecase import (
    ManualRecordQueryUseCase,
)
from dddpy.manual_record.usecase.manual_record_factory import (
    manual_record_cmd_usecase_factory,
    manual_record_query_usecase_factory,
)
from dddpy.manual_record.usecase.manual_record_cmd_schema import (
    CreateManualRecordSchema,
    UpdateManualRecordSchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("manual_record_usecase")

from dddpy.manual_record.domain.manual_record_exception import ManualRecordNotFound
from dddpy.manual_record.domain.manual_record_success import ManualRecordSucessMessage


class ManualRecordUseCase:
    def __init__(self):
        logging.info("__init__")
        self.manual_record_cmd_usecase: ManualRecordCmdUseCase = (
            manual_record_cmd_usecase_factory()
        )
        self.manual_record_query_usecase: ManualRecordQueryUseCase = (
            manual_record_query_usecase_factory()
        )
        logging.info("ManualRecordUseCase initialized")

    def create(self, manual_record_data: CreateManualRecordSchema):
        logging.info("create")
        logging.info(f"Creating a new manual_record with data: {manual_record_data}")

        new_manual_record = self.manual_record_cmd_usecase.create(manual_record_data)
        success = ResponseSuccessSchema(
            success=True,
            message=ManualRecordSucessMessage.COMPANY_CREATED,
            data=new_manual_record.to_dict(),
        )
        logging.info(f"ManualRecord created successfully: {success}")
        return success

    def get_by_id(self, id: str):
        logging.info("get_by_id")
        manual_record = self.manual_record_query_usecase.get_by_id(id)
        if not manual_record:
            raise ManualRecordNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ManualRecordSucessMessage.COMPANY_GET,
            data=manual_record.to_dict(),
        )
        logging.info(f"ManualRecord retrieved successfully by id={id}")
        return success

    def get_by_manual_record_brand_id(self, manual_record_brand_id: str):
        logging.info("get_by_code")
        manual_record = self.manual_record_query_usecase.get_by_manual_record_brand_id(
            manual_record_brand_id
        )

        success = ResponseSuccessSchema(
            success=True,
            message=ManualRecordSucessMessage.COMPANY_GET,
            data=manual_record.to_dict(),
        )
        logging.info(
            f"ManualRecord retrieved successfully by brand_id={manual_record_brand_id}"
        )
        return success

    def update(self, id: str, manual_record_data: UpdateManualRecordSchema):
        logging.info("update")
        logging.info(f"Updating manual_record {id} with data: {manual_record_data}")

        updated_manual_record = self.manual_record_cmd_usecase.update(
            id, manual_record_data
        )
        if not updated_manual_record:
            raise ManualRecordNotFound()

        success = ResponseSuccessSchema(
            success=True,
            message=ManualRecordSucessMessage.COMPANY_UPDATED,
            data=updated_manual_record.to_dict(),
        )
        logging.info(f"ManualRecord updated successfully: {success}")
        return success

    def list_all(self):
        logging.info("list_all")
        manual_record = self.manual_record_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=ManualRecordSucessMessage.COMPANYS_GET,
            data=[c.to_dict() for c in manual_record],
        )
        logging.info(
            f"ManualRecords listed successfully: {len(manual_record)} manual_record"
        )
        return success
