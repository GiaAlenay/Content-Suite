from dddpy.content_log.usecase.content_log_cmd_usecase import ContentLogCmdUseCase
from dddpy.content_log.usecase.content_log_query_usecase import ContentLogQueryUseCase

# from dddpy.content_log.usecase.content_log_factory import (
#     content_log_cmd_usecase_factory,
#     content_log_query_usecase_factory,
# )
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
    ContentLogNotAllowedToChangeStatus,
)
from dddpy.content_log.domain.content_log_success import ContentLogSucessMessage

# from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.brand.usecase.brand_query_usecase import (
    BrandQueryUseCase,
)

# from dddpy.brand.usecase.brand_factory import brand_query_usecase_factory
from dddpy.brand.domain.brand_exception import BrandNotFound
from dddpy.content_log.usecase.creative_agent import (
    CreativeEngineAgent,
)
from dddpy.content_log.usecase.governance_audit_agent import (
    GovernanceAuditAgent,
)

# from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
#     BrandManualVectorQueryUseCase,
# )
# from dddpy.brand_manual_vector.usecase.brand_manual_vector_factory import (
#     brand_manual_vector_query_usecase_factory,
# )


class ContentLogUseCase:

    def __init__(
        self,
        content_log_cmd: ContentLogCmdUseCase,
        content_log_query: ContentLogQueryUseCase,
        brand_query: BrandQueryUseCase,
        content_generator: CreativeEngineAgent,
        auditor: GovernanceAuditAgent,
    ):
        self.content_log_cmd_usecase = content_log_cmd
        self.content_log_query_usecase = content_log_query
        self.brand_query_usecase = brand_query
        self.content_generator = content_generator
        self.auditor = auditor
        logging.info("ContentLogUseCase initialized with injected dependencies")

    def create(
        self,
        brand_id: str,
        content_log_request: GenerateContentRequest,
        creator_id: str,
    ):
        brand = self.brand_query_usecase.get_by_id(brand_id)
        if not brand or brand.status != "ACTIVE":
            raise BrandNotFound()

        text = self.content_generator.generate_content(
            user_prompt=content_log_request.user_prompt,
            brand_name=brand.name,
            brand_id=brand_id,
            content_type=content_log_request.content_type,
        )

        to_create_content_log = CreateContentLogSchema(
            brand_id=brand_id,
            prompt_origin=content_log_request.user_prompt,
            creator_id=creator_id,
            status="PENDING",
            content_data={"text": text},
            content_type=content_log_request.content_type,
        )
        return self.content_log_cmd_usecase.create(to_create_content_log)

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

    def auditar_multimodal(self, brand_id: str, file_url: str, user_id: str):

        logging.info(f"Iniciando auditoría multimodal para brand_id={brand_id}")
        audit_result = self.auditor.audit_image_compliance(
            file_url=file_url, brand_id=brand_id
        )

        to_create_content_log = CreateContentLogSchema(
            brand_id=brand_id,
            creator_id=user_id,
            status=audit_result["suggested_status"],
            content_type="IMAGE_AUDIT",
            content_data={"image_url": file_url},
            agent_feedback=audit_result["feedback"],
            audit_by=user_id,
        )

        new_log = self.content_log_cmd_usecase.create(to_create_content_log)

        return ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.CONTENTLOG_CREATED_AUDITED,
            data={"audit": audit_result, "new_content_log_id": new_log.id},
        )

    def auditar_texto(
        self,
        id: str,
    ):
        logging.info("update")
        logging.info(f"Audit content_log by id={id} ")
        content_log = self.content_log_query_usecase.get_by_id(id)
        if not content_log:
            raise ContentLogNotFound()

        if content_log.status != "PENDING":
            raise ContentLogNotAllowedToChangeStatus()

        audit_result = self.auditor.audit_text_compliance(
            content_to_audit=content_log.content_data["text"],
            brand_id=content_log.brand_id,
        )
        success = ResponseSuccessSchema(
            success=True,
            message=ContentLogSucessMessage.CONTENTLOG_AUDITED,
            data=audit_result.model_dump(),
        )
        logging.info(f"ContentLog updated successfully: {success}")
        return success

    def update_audited_information(
        self, id: str, content_log_data: UpdateContentLogSchema, user_id: str
    ):
        logging.info("update")
        logging.info(f"Updating content_log {id} with data: {content_log_data}")
        content_log = self.content_log_query_usecase.get_by_id(id)
        content_log_data.audit_by = user_id
        if not content_log:
            raise ContentLogNotFound()

        if content_log.status != "PENDING":
            raise ContentLogNotAllowedToChangeStatus()

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
