from typing import Optional, List
from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_query_repository import (
    BrandManualVectorQueryRepository,
)
from dddpy.brand_manual_vector.infrastructure.brand_manual_vector_mapper import (
    BrandManualVectorMapper,
)

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("BrandManualVectorCmdRepositoryImpl")


class BrandManualVectorQueryRepositoryImpl(BrandManualVectorQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "companies_companies"
        logging.info("BrandManualVectorQueryRepositoryImpl initialized with Supabase")

    def get_by_id(self, id: str) -> Optional[BrandManualVectorEntity]:
        logging.info(f"Fetching brand_manual_vector with id={id}", method="get_by_id")
        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )

        db_brand_manual_vector = response.data
        return (
            BrandManualVectorMapper.to_domain(db_brand_manual_vector)
            if db_brand_manual_vector
            else None
        )

    def get_by_brand_id(self, brand_id: str) -> Optional[BrandManualVectorEntity]:
        logging.info(
            f"Fetching brand_manual_vector with brand_id={brand_id}",
            method="get_by_brand_id",
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", brand_id)
            .maybe_single()
            .execute()
        )

        db_brand_manual_vector = response.data
        return (
            BrandManualVectorMapper.to_domain(db_brand_manual_vector)
            if db_brand_manual_vector
            else None
        )

    def list_all(self) -> List[BrandManualVectorEntity]:
        logging.info("Fetching all companies", method="list_all")

        response = self._client.table(self._table).select("*").execute()

        db_brand_manual_vectors = (
            response.data
        )  # response.data es una lista de diccionarios
        return [BrandManualVectorMapper.to_domain(db) for db in db_brand_manual_vectors]
