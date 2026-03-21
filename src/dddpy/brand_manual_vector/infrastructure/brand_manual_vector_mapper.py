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
            brand_id=db_dict.get("brand_id", "Sin nombre"),
            content_chunk=db_dict.get("content_chunk"),
            embedding=db_dict.get("embedding"),
            raw_parameters=db_dict.get("raw_parameters", {}),
            metadata=db_dict.get("metadata", 1),
            creator_id=db_dict.get("creator_id"),
            status=db_dict.get("status", "ACTIVE"),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure(entity: BrandManualVectorEntity) -> dict:
        return {
            "brand_id": entity.brand_id,
            "content_chunk": entity.content_chunk,
            "embedding": entity.embedding,
            "raw_parameters": entity.raw_parameters,
            "metadata": entity.metadata,
            "creator_id": entity.creator_id,
            "status": entity.status,
        }

    @staticmethod
    def to_infrastructure_from_create(
        brand_manual_vector: CreateBrandManualVectorData,
    ) -> dict:
        """Mapea el DataClass de creación al formato de tabla de Supabase"""
        return {
            "brand_id": brand_manual_vector.brand_id,
            "content_chunk": brand_manual_vector.content_chunk,
            "embedding": brand_manual_vector.embedding,
            "raw_parameters": brand_manual_vector.raw_parameters,
            "creator_id": brand_manual_vector.creator_id,
            "metadata": brand_manual_vector.metadata,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateBrandManualVectorData) -> dict:
        """Mapea solo los campos que no son None para la actualización."""
        raw_map = {
            "status": data.status,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
