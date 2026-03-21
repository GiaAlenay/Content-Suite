from dddpy.brand.domain.brand_entity import BrandEntity


class BrandMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> BrandEntity:
        return BrandEntity(
            id=db_dict.get("id"),
            name=db_dict.get("name", "Sin nombre"),
            code=db_dict.get("code", "").upper(),
            full_manual=db_dict.get("full_manual"),
            created_at=db_dict.get("created_at"),
        )

    @staticmethod
    def to_infrastructure(entity: BrandEntity) -> dict:
        return {
            "name": entity.name,
            "code": entity.code,
            "full_manual": entity.full_manual,
            "description": entity.description,
        }
