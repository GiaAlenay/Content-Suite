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
            brand_id=db_dict.get("brand_id", ""),
            creator_id=db_dict.get("creator_id", ""),
            content_data=db_dict.get("content_data"),
            content_type=db_dict.get("content_type"),
            agent_feedback=db_dict.get("agent_feedback", ""),
            audit_by=db_dict.get("audit_by"),
            status=db_dict.get("status", ""),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure(entity: ContentLogEntity) -> dict:
        return {
            "brand_id": entity.brand_id,
            "creator_id": entity.creator_id,
            "content_data": entity.content_data,
            "content_type": entity.content_type,
            "agent_feedback": entity.agent_feedback,
            "audit_by": entity.audit_by,
            "status": entity.status,
        }

    @staticmethod
    def to_infrastructure_from_create(content_log: CreateContentLogData) -> dict:
        """Mapea el DataClass de creación al formato de tabla de Supabase"""
        return {
            "brand_id": content_log.brand_id,
            "creator_id": content_log.creator_id,
            "content_data": content_log.content_data,
            "content_type": content_log.content_type,
            "agent_feedback": content_log.agent_feedback,
            "audit_by": content_log.audit_by,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateContentLogData) -> dict:
        """Mapea solo los campos que no son None para la actualización."""
        raw_map = {
            "agent_feedback": data.agent_feedback,
            "audit_by": data.audit_by,
            "status": data.status,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
