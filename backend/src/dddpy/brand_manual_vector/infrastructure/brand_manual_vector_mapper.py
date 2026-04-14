from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_data import (
    CreateBrandManualVectorData,
    UpdateBrandManualVectorData,
)


class BrandManualVectorMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> BrandManualVectorEntity:
        return BrandManualVectorEntity(
            id=db_dict.get("id"),
            manual_version_id=db_dict.get("manual_version_id"),
            manual_section_id=db_dict.get("manual_section_id"),
            content_chunk=db_dict.get("content_chunk"),
            embedding=db_dict.get("embedding"),
            metadata=db_dict.get("metadata", {}),
            status=db_dict.get("status", "draft"),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(data: CreateBrandManualVectorData) -> dict:
        return {
            "manual_version_id": data.manual_version_id,
            "manual_section_id": data.manual_section_id,
            "content_chunk": data.content_chunk,
            "embedding": data.embedding,
            "metadata": data.metadata or {},
            "status": data.status,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateBrandManualVectorData) -> dict:
        raw_map = {
            "metadata": data.metadata,
            "status": data.status,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
