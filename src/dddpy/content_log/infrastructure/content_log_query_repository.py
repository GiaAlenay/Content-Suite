from typing import Optional, List
from dddpy.content_log.domain.content_log_entity import ContentLogEntity
from dddpy.content_log.domain.content_log_query_repository import (
    ContentLogQueryRepository,
)
from dddpy.content_log.infrastructure.content_log_mapper import ContentLogMapper

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("ContentLogCmdRepositoryImpl")


class ContentLogQueryRepositoryImpl(ContentLogQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "content_log"
        logging.info("ContentLogQueryRepositoryImpl initialized with Supabase")

    def get_by_id(self, id: str) -> Optional[ContentLogEntity]:
        logging.info(f"Fetching content_log with id={id}", method="get_by_id")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if not response or not response.data:
            return None

        db_content_log = response.data
        return ContentLogMapper.to_domain(db_content_log) if db_content_log else None

    def get_by_content_log_brand_id(
        self, content_log_brand_id: str
    ) -> List[ContentLogEntity]:
        logging.info(
            f"Fetching content_log with content_log_brand_id={content_log_brand_id}",
            method="get_by_content_log_brand_id",
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", content_log_brand_id)
            .execute()
        )

        db_content_log = response.data
        return ContentLogMapper.to_domain(db_content_log) if db_content_log else None

    def list_all(self) -> List[ContentLogEntity]:
        logging.info("Fetching all  ", method="list_all")

        response = self._client.table(self._table).select("*").execute()

        db_content_logs = response.data  # response.data es una lista de diccionarios
        return [ContentLogMapper.to_domain(db) for db in db_content_logs]
