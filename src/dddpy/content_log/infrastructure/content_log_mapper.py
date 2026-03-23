from dddpy.content_log.domain.content_log_entity import ContentLogEntity
from dddpy.content_log.domain.content_log_data import (
    CreateContentLogData,
    UpdateContentLogData,
)


class ContentLogMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> ContentLogEntity:
        return ContentLogEntity(
            id=db_dict.get("id"),
            brand_id=db_dict.get("brand_id"),
            creator_id=db_dict.get("creator_id"),
            content_data=db_dict.get("content_data", {}),
            content_type=db_dict.get("content_type"),
            status=db_dict.get("status", "PENDING"),
            agent_feedback=db_dict.get("agent_feedback"),
            audit_by=db_dict.get("audit_by"),
            prompt_origin=db_dict.get("prompt_origin"),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(data: CreateContentLogData) -> dict:
        return {
            "brand_id": data.brand_id,
            "creator_id": data.creator_id,
            "content_data": data.content_data,
            "content_type": data.content_type,
            "status": data.status,
            "agent_feedback": data.agent_feedback,
            "audit_by": data.audit_by,
            "prompt_origin": data.prompt_origin,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateContentLogData) -> dict:

        raw_map = {
            "status": data.status,
            "agent_feedback": data.agent_feedback,
            "audit_by": data.audit_by,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
