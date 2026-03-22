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
            brand_id=db_dict.get("brand_id"),
            manual_record_id=db_dict.get("manual_record_id"),
            content_chunk=db_dict.get("content_chunk"),
            embedding=db_dict.get("embedding"),
            creator_id=db_dict.get("creator_id"),
            metadata=db_dict.get("metadata", {}),
            status=db_dict.get("status", ""),
            created_at=db_dict.get("created_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(data: CreateBrandManualVectorData) -> dict:
        return {
            "brand_id": data.brand_id,
            "manual_record_id": data.manual_record_id,
            "content_chunk": data.content_chunk,
            "embedding": data.embedding,
            "creator_id": data.creator_id,
            "metadata": data.metadata,
            "status": "ACTIVE",
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateBrandManualVectorData) -> dict:
        raw_map = {
            "status": data.status,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
