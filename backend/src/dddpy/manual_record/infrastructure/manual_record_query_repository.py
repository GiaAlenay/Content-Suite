from typing import Optional, List
from dddpy.manual_record.domain.manual_record_entity import ManualRecordEntity
from dddpy.manual_record.domain.manual_record_query_repository import (
    ManualRecordQueryRepository,
)
from dddpy.manual_record.infrastructure.manual_record_mapper import ManualRecordMapper

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("ManualRecordCmdRepositoryImpl")


class ManualRecordQueryRepositoryImpl(ManualRecordQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "manual_record"
        logging.info("ManualRecordQueryRepositoryImpl initialized with Supabase")

    def get_by_id(self, id: str) -> Optional[ManualRecordEntity]:
        logging.info(f"Fetching manual_record with id={id}")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if not response or not response.data:
            return None

        db_manual_record = response.data
        return (
            ManualRecordMapper.to_domain(db_manual_record) if db_manual_record else None
        )

    def get_by_manual_record_brand_id(
        self, manual_record_brand_id: str
    ) -> List[ManualRecordEntity]:
        logging.info(
            f"Fetching manual_record with manual_record_brand_id={manual_record_brand_id}"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", manual_record_brand_id)
            .execute()
        )

        db_manual_record = response.data
        return (
            ManualRecordMapper.to_domain(db_manual_record) if db_manual_record else None
        )

    def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ManualRecordEntity]:
        logging.info(
            f"Fetching latest version of manual_record with brand_id={brand_id}"
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
            return ManualRecordMapper.to_domain(db_records[0])

        return None

    def list_all(self) -> List[ManualRecordEntity]:
        logging.info("Fetching all  ")

        response = self._client.table(self._table).select("*").execute()

        db_manual_records = response.data
        return [ManualRecordMapper.to_domain(db) for db in db_manual_records]
