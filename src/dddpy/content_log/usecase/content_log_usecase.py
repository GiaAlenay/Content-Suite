from dddpy.content_log.usecase.content_log_cmd_usecase import ContentLogCmdUseCase
from dddpy.content_log.usecase.content_log_query_usecase import ContentLogQueryUseCase
from dddpy.content_log.usecase.content_log_factory import (
    content_log_cmd_usecase_factory,
    content_log_query_usecase_factory,
)
from dddpy.content_log.usecase.content_log_cmd_schema import (
    CreateContentLogSchema,
    UpdateContentLogSchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("content_log_usecase")

from dddpy.content_log.domain.content_log_exception import (
    ContentLogNotFound,
    RepeatedContentLogCode,
    RepeatedContentLogName,
)
from dddpy.content_log.domain.content_log_success import ContentLogSucessMessage


class ContentLogUseCase:
    def __init__(self):
        logging.info("__init__")
        self.content_log_cmd_usecase: ContentLogCmdUseCase = (
            content_log_cmd_usecase_factory()
        )
        self.content_log_query_usecase: ContentLogQueryUseCase = (
            content_log_query_usecase_factory()
        )
        logging.info("ContentLogUseCase initialized")

    def create(self, content_log_data: CreateContentLogSchema):
        logging.info("create")
        logging.info(f"Creating a new content_log with data: {content_log_data}")

        existing_content_data = self.content_log_query_usecase.get_by_content_data(
            content_log_data.content_data
        )
        existing_content_log_brand_id = (
            self.content_log_query_usecase.get_by_content_log_brand_id(
                content_log_data.brand_id
            )
        )
        if existing_content_data:
            raise RepeatedContentLogCode()
        if existing_content_log_brand_id:
            raise RepeatedContentLogName()

        new_content_log = self.content_log_cmd_usecase.create(content_log_data)
        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.COMPANY_CREATED,
            data=new_content_log.to_dict(),
        )
        logging.info(f"ContentLog created successfully: {success}")
        return success

    def get_by_id(self, id: str):
        logging.info("get_by_id")
        content_log = self.content_log_query_usecase.get_by_id(id)
        if not content_log:
            raise ContentLogNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.COMPANY_GET,
            data=content_log.to_dict(),
        )
        logging.info(f"ContentLog retrieved successfully by id={id}")
        return success

    def get_by_content_data(self, content_data: str):
        logging.info("get_by_content_data")
        content_log = self.content_log_query_usecase.get_by_content_data(content_data)
        if not content_log:
            raise ContentLogNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.COMPANY_GET,
            data=content_log.to_dict(),
        )
        logging.info(f"ContentLog retrieved successfully by id={id}")
        return success

    def get_by_content_log_brand_id(self, content_log_brand_id: str):
        logging.info("get_by_content_data")
        content_log = self.content_log_query_usecase.get_by_content_log_brand_id(
            content_log_brand_id
        )
        if not content_log:
            raise ContentLogNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.COMPANY_GET,
            data=content_log.to_dict(),
        )
        logging.info(
            f"ContentLog retrieved successfully by brand_id={content_log_brand_id}"
        )
        return success

    def update(self, id: str, content_log_data: UpdateContentLogSchema):
        logging.info("update")
        logging.info(f"Updating content_log {id} with data: {content_log_data}")

        if content_log_data.brand_id:
            existing_content_log_brand_id = (
                self.content_log_query_usecase.get_by_content_log_brand_id(
                    content_log_data.brand_id
                )
            )
            if existing_content_log_brand_id:
                raise RepeatedContentLogName()

        updated_content_log = self.content_log_cmd_usecase.update(id, content_log_data)
        if not updated_content_log:
            raise ContentLogNotFound()

        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.COMPANY_UPDATED,
            data=updated_content_log.to_dict(),
        )
        logging.info(f"ContentLog updated successfully: {success}")
        return success

    def delete(self, id: str):
        logging.info("delete")
        logging.info(f"Deleting content_log {id}")

        deleted = self.content_log_cmd_usecase.delete(id)
        if not deleted:
            raise ContentLogNotFound()
        success = ResponseSuccessSchema(
            success=True, message=ContentLogSucessMessage.COMPANY_DELETED, data={}
        )
        logging.info(f"ContentLog deleted successfully: {success}")
        return success

    def list_all(self):
        logging.info("list_all")
        content_log = self.content_log_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.COMPANYS_GET,
            data=[c.to_dict() for c in content_log],
        )
        logging.info(f"ContentLogs listed successfully: {len(content_log)} content_log")
        return success
