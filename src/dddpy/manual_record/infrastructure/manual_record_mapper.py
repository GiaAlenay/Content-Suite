from dddpy.manual_record.domain.manual_record_entity import ManualRecordEntity
from dddpy.manual_record.domain.manual_record_data import (
    CreateManualRecordData,
    UpdateManualRecordData,
)


class ManualRecordMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> ManualRecordEntity:
        return ManualRecordEntity(
            id=db_dict.get("id"),
            brand_id=db_dict.get("brand_id"),
            version=db_dict.get("version"),
            full_manual=db_dict.get("full_manual"),
            raw_parameters=db_dict.get("raw_parameters", {}),
            is_current_version=db_dict.get("is_current_version", False),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(data: CreateManualRecordData) -> dict:
        return {
            "brand_id": data.brand_id,
            "version": data.version,
            "full_manual": data.full_manual,
            "raw_parameters": data.raw_parameters,
            "is_current_version": data.is_current_version,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateManualRecordData) -> dict:
        raw_map = {
            "is_current_version": data.is_current_version,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
