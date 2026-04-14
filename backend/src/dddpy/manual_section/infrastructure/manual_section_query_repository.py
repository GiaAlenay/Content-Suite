from typing import Optional, List
from dddpy.manual_section.domain.manual_section_entity import ManualSectionEntity
from dddpy.manual_section.domain.manual_section_query_repository import (
    ManualSectionQueryRepository,
)
from dddpy.manual_section.infrastructure.manual_section_mapper import (
    ManualSectionMapper,
)

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("ManualSectionCmdRepositoryImpl")


class ManualSectionQueryRepositoryImpl(ManualSectionQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "manual_sections"
        logging.info("ManualSectionQueryRepositoryImpl initialized with Supabase")

    async def get_by_id(self, id: str) -> Optional[ManualSectionEntity]:
        logging.info(f"Fetching manual_section with id={id}")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if not response or not response.data:
            return None

        db_manual_section = response.data
        return (
            ManualSectionMapper.to_domain(db_manual_section)
            if db_manual_section
            else None
        )

    async def get_by_manual_section_brand_id(
        self, manual_section_brand_id: str
    ) -> List[ManualSectionEntity]:
        logging.info(
            f"Fetching manual_section with manual_section_brand_id={manual_section_brand_id}"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", manual_section_brand_id)
            .execute()
        )

        db_manual_section = response.data
        return (
            ManualSectionMapper.to_domain(db_manual_section)
            if db_manual_section
            else None
        )

    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ManualSectionEntity]:
        logging.info(
            f"Fetching latest version of manual_section with brand_id={brand_id}"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", brand_id)
            .eq("is_current_version", True)
            .limit(1)
            .execute()
        )

        db_records = response.data

        if db_records and len(db_records) > 0:
            return ManualSectionMapper.to_domain(db_records[0])

        return None

    async def list_all(self) -> List[ManualSectionEntity]:
        logging.info("Fetching all  ")

        response = await self._client.table(self._table).select("*").execute()

        db_manual_sections = response.data
        return [ManualSectionMapper.to_domain(db) for db in db_manual_sections]
