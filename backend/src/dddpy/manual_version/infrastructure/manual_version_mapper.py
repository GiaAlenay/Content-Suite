from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity
from dddpy.manual_version.domain.manual_version_data import (
    CreateManualVersionData,
    UpdateManualVersionData,
)


class ManualVersionMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> ManualVersionEntity:
        return ManualVersionEntity(
            id=db_dict.get("id"),
            brand_id=db_dict.get("brand_id"),
            version_number=db_dict.get("version_number"),
            full_content=db_dict.get("full_content"),
            raw_parameters=db_dict.get("raw_parameters", {}),
            status=db_dict.get("status", "draft"),
            url_pdf_manual=db_dict.get("url_pdf_manual"),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(data: CreateManualVersionData) -> dict:
        return {
            "brand_id": data.brand_id,
            "version_number": data.version_number,
            "full_content": data.full_content,
            "raw_parameters": data.raw_parameters,
            "status": data.status,
            "url_pdf_manual": data.url_pdf_manual,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateManualVersionData) -> dict:
        raw_map = {
            "status": data.status,
            "url_pdf_manual": data.url_pdf_manual,
            "full_content": data.full_content,
            "raw_parameters": data.raw_parameters,
        }
        return {k: v for k, v in raw_map.items() if v is not None}
