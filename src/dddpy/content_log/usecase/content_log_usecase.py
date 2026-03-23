from dddpy.content_log.usecase.content_log_cmd_usecase import ContentLogCmdUseCase
from dddpy.content_log.usecase.content_log_query_usecase import ContentLogQueryUseCase
from dddpy.content_log.usecase.content_log_factory import (
    content_log_cmd_usecase_factory,
    content_log_query_usecase_factory,
)
from dddpy.content_log.usecase.content_log_cmd_schema import (
    CreateContentLogSchema,
    GenerateContentRequest,
    UpdateContentLogSchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("content_log_usecase")

from dddpy.content_log.domain.content_log_exception import (
    ContentLogNotFound,
)
from dddpy.content_log.domain.content_log_success import ContentLogSucessMessage
from src.dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.brand.usecase.brand_query_usecase import (
    BrandQueryUseCase,
)
from dddpy.brand.usecase.brand_factory import brand_query_usecase_factory
from dddpy.brand.domain.brand_exception import BrandNotFound
from dddpy.content_log.usecase.content_generator_service import CreativeEngineService
from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_factory import (
    brand_manual_vector_query_usecase_factory,
)


class ContentLogUseCase:
    def __init__(self):
        logging.info("__init__")
        self.content_log_cmd_usecase: ContentLogCmdUseCase = (
            content_log_cmd_usecase_factory()
        )
        self.content_log_query_usecase: ContentLogQueryUseCase = (
            content_log_query_usecase_factory()
        )

        self.brand_manual_vector_query_usecase: BrandManualVectorQueryUseCase = (
            brand_manual_vector_query_usecase_factory()
        )
        self.vectorize = VectorizationService()
        self.brand_query_usecase: BrandQueryUseCase = brand_query_usecase_factory()
        self.conten_generator = CreativeEngineService()
        logging.info("ContentLogUseCase initialized")

    def create(self, brand_id: str, content_log_request: GenerateContentRequest):
        logging.info("create")
        logging.info(f"Creating a new content_log with data: {content_log_request}")

        brand = self.brand_query_usecase.get_by_id(brand_id)
        if not brand or brand.status != "ACTIVE":
            raise BrandNotFound()

        query_vector = self.vectorize.prepare_vector_for_user_prompt(
            content_log_request.user_prompt
        )

        relevant_chunks = self.brand_manual_vector_query_usecase.search_brand_context(
            brand_id=brand_id, vector=query_vector
        )
        context_text = "\n".join([chunk.content_chunk for chunk in relevant_chunks])

        text = self.conten_generator.generate_content_with_rag(
            user_prompt=content_log_request.user_prompt,
            brand_name=brand.name,
            context_chunks=context_text,
            content_type=content_log_request.content_type,
        )

        to_create_content_log = CreateContentLogSchema(
            brand_id=brand_id,
            creator_id="e125dc69-eb45-4af8-8343-57092522f3fe",
            prompt_origin=content_log_request.user_prompt,
            status="PENDING",
            content_type=content_log_request.content_type,
            content_data={"text": text},
        )

        new_content_log = self.content_log_cmd_usecase.create(to_create_content_log)
        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.CONTENTLOG_CREATED,
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
            message=ContentLogSucessMessage.CONTENTLOG_GET,
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
            message=ContentLogSucessMessage.CONTENTLOG_GET,
            data=content_log.to_dict(),
        )
        logging.info(
            f"ContentLog retrieved successfully by brand_id={content_log_brand_id}"
        )
        return success

    def update(self, id: str, content_log_data: UpdateContentLogSchema):
        logging.info("update")
        logging.info(f"Updating content_log {id} with data: {content_log_data}")

        updated_content_log = self.content_log_cmd_usecase.update(id, content_log_data)

        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.CONTENTLOG_UPDATED,
            data=updated_content_log.to_dict(),
        )
        logging.info(f"ContentLog updated successfully: {success}")
        return success

    def list_all(self):
        logging.info("list_all")
        content_log = self.content_log_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.CONTENTLOGS_GET,
            data=[c.to_dict() for c in content_log],
        )
        logging.info(f"ContentLogs listed successfully: {len(content_log)} content_log")
        return success
