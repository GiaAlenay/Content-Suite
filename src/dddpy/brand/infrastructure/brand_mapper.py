from dddpy.brand.domain.brand_entity import BrandEntity
from dddpy.brand.domain.brand_data import (
    CreateBrandData,
    UpdateBrandData,
)
from typing import Optional


class BrandMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> Optional[BrandEntity]:
        return BrandEntity(
            id=db_dict.get("id"),
            name=db_dict.get("name", "Sin nombre"),
            code=db_dict.get("code", "").upper(),
            description=db_dict.get("description"),
            logo_url=db_dict.get("logo_url"),
            status=db_dict.get("status", "ACTIVE"),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(brand: CreateBrandData) -> dict:
        return {
            "name": brand.name,
            "code": brand.code.upper(),
            "description": brand.description,
            "logo_url": brand.logo_url,
            "status": "ACTIVE",
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateBrandData) -> dict:
        raw_map = {
            "name": data.name,
            "description": data.description,
            "logo_url": data.logo_url,
            "status": data.status,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
