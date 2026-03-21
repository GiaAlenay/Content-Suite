from dddpy.brand.domain.brand_entity import BrandEntity
from dddpy.brand.domain.brand_data import (
    CreateBrandData,
    UpdateBrandData,
)


class BrandMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> BrandEntity:
        return BrandEntity(
            id=db_dict.get("id"),
            code=db_dict.get("code", "").upper(),
            name=db_dict.get("name", "Sin nombre"),
            description=db_dict.get("description"),
            full_manual=db_dict.get("full_manual"),
            raw_parameters=db_dict.get("raw_parameters", {}),
            current_version=db_dict.get("current_version", 1),
            logo_url=db_dict.get("logo_url"),
            status=db_dict.get("status", "ACTIVE"),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure(entity: BrandEntity) -> dict:
        return {
            "code": entity.code,
            "name": entity.name,
            "description": entity.description,
            "full_manual": entity.full_manual,
            "raw_parameters": entity.raw_parameters,
            "current_version": entity.current_version,
            "logo_url": entity.logo_url,
            "status": entity.status,
        }

    @staticmethod
    def to_infrastructure_from_create(brand: CreateBrandData) -> dict:
        """Mapea el DataClass de creación al formato de tabla de Supabase"""
        return {
            "name": brand.name,
            "code": brand.code.upper(),
            "description": brand.description,
            "full_manual": brand.full_manual,
            "raw_parameters": brand.raw_parameters,  # No olvides este
            "logo_url": brand.logo_url,
            "current_version": brand.current_version,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateBrandData) -> dict:
        """Mapea solo los campos que no son None para la actualización."""
        raw_map = {
            "name": data.name,
            "description": data.description,
            "full_manual": data.full_manual,
            "logo_url": data.logo_url,
            "status": data.status,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
