from dddpy.content_log.usecase.content_log_cmd_schema import (
    CreateContentLogSchema,
    UpdateContentLogSchema,
)
from dddpy.content_log.domain.content_log_data import (
    CreateContentLogData,
    UpdateContentLogData,
)

from dddpy.content_log.domain.content_log_cmd_repository import ContentLogCmdRepository
from dddpy.content_log.domain.content_log_entity import ContentLogEntity

from typing import Optional
from dddpy.shared.logging.logging import Logger

logging = Logger("ContentLogCmdUseCase")


class ContentLogCmdUseCase:

    def __init__(self, repository: ContentLogCmdRepository):
        self.repository = repository
        logging.info("ContentLogCmdUseCase initialized")

    def create(self, content_log_data: CreateContentLogSchema):
        logging.info(
            f"Delegating content_log creation for content_data={content_log_data.content_data}"
        )
        data = CreateContentLogData(
            creator_id=content_log_data.creator_id,
            brand_id=content_log_data.brand_id,
            content_type=content_log_data.content_type,
            content_data=content_log_data.content_data,
            agent_feedback=content_log_data.agent_feedback,
            audit_by=content_log_data.audit_by,
            status=content_log_data.status,
            prompt_origin=content_log_data.prompt_origin,
            parent_id=content_log_data.parent_id,
        )

        return self.repository.create(data)

    def update(
        self, id: str, content_log_data: UpdateContentLogSchema
    ) -> Optional[ContentLogEntity]:
        logging.info(f"Delegating content_log update for id={id}")
        data = UpdateContentLogData(
            audit_by=content_log_data.audit_by,
            status=content_log_data.status,
            agent_feedback=content_log_data.agent_feedback,
        )
        return self.repository.update(id, data)

    def delete(self, id: str) -> bool:
        logging.info(f"Delegating content_log delete for id={id}")
        return self.repository.delete(id)
