from typing import Optional, List
from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity
from dddpy.manual_version.domain.manual_version_query_repository import (
    ManualVersionQueryRepository,
)
from dddpy.manual_version.infrastructure.manual_version_mapper import (
    ManualVersionMapper,
)

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("ManualVersionCmdRepositoryImpl")


class ManualVersionQueryRepositoryImpl(ManualVersionQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "manual_version"
        logging.info("ManualVersionQueryRepositoryImpl initialized with Supabase")

    async def get_by_id(self, id: str) -> Optional[ManualVersionEntity]:
        logging.info(f"Fetching manual_version with id={id}")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if not response or not response.data:
            return None

        db_manual_version = response.data
        return (
            ManualVersionMapper.to_domain(db_manual_version)
            if db_manual_version
            else None
        )

    async def get_by_manual_version_brand_id(
        self, manual_version_brand_id: str
    ) -> List[ManualVersionEntity]:
        logging.info(
            f"Fetching manual_version with manual_version_brand_id={manual_version_brand_id}"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", manual_version_brand_id)
            .execute()
        )

        db_manual_version = response.data
        return (
            ManualVersionMapper.to_domain(db_manual_version)
            if db_manual_version
            else None
        )

    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ManualVersionEntity]:
        logging.info(
            f"Fetching latest version of manual_version (highest version_number) with brand_id={brand_id}"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", brand_id)
            .neq("status", "INACTIVE")
            .order("version_number", desc=True)
            .limit(1)
            .execute()
        )

        db_records = response.data

        if db_records and len(db_records) > 0:
            return ManualVersionMapper.to_domain(db_records[0])

        return None

    async def list_all(self) -> List[ManualVersionEntity]:
        logging.info("Fetching all  ")

        response = await self._client.table(self._table).select("*").execute()

        db_manual_versions = response.data
        return [ManualVersionMapper.to_domain(db) for db in db_manual_versions]
