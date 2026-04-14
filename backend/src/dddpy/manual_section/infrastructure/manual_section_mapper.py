from dddpy.manual_section.domain.manual_section_entity import ManualSectionEntity
from dddpy.manual_section.domain.manual_section_data import (
    CreateManualSectionData,
    UpdateManualSectionData,
)


class ManualSectionMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> ManualSectionEntity:
        return ManualSectionEntity(
            id=db_dict.get("id"),
            manual_version_id=db_dict.get("manual_version_id"),
            section_name=db_dict.get("section_name"),
            content=db_dict.get("content"),
            order_number=db_dict.get("order_number"),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(data: CreateManualSectionData) -> dict:
        return {
            "manual_version_id": data.manual_version_id,
            "section_name": data.section_name,
            "content": data.content,
            "order_number": data.order_number,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateManualSectionData) -> dict:
        raw_map = {
            "section_name": data.section_name,
            "content": data.content,
            "order": data.order_number,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
