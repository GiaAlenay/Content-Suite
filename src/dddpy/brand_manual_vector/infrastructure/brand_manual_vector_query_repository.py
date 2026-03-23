from typing import Optional, List
from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
    BrandManualVectorSimilarityEntity,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_query_repository import (
    BrandManualVectorQueryRepository,
)
from dddpy.brand_manual_vector.infrastructure.brand_manual_vector_mapper import (
    BrandManualVectorMapper,
)

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("BrandManualVectorQueryRepositoryImpl")


class BrandManualVectorQueryRepositoryImpl(BrandManualVectorQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "brand_manuals_vectors"
        logging.info("BrandManualVectorQueryRepositoryImpl initialized with Supabase")

    def search_brand_context(self, brand_id: str, vector: list[float], limit: int = 3):
        logging.info(f"Invocando RPC match_brand_manuals para brand: {brand_id}")

        rpc_params = {
            "query_embedding": vector,
            "match_threshold": 0.5,
            "match_count": limit,
            "target_brand_id": brand_id,
        }

        response = self._client.rpc("match_brand_manuals", rpc_params).execute()

        if not response or not response.data:
            logging.warning("No se encontró contexto relevante en el manual.")
            return []

        return [
            BrandManualVectorSimilarityEntity(
                id=item["id"],
                content_chunk=item["content_chunk"],
                similarity=item["similarity"],
            )
            for item in response.data
        ]

    def get_by_id(self, id: str) -> Optional[BrandManualVectorEntity]:
        logging.info(f"Fetching brand_manual_vector with id={id}", method="get_by_id")
        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if not response or not response.data:
            return None

        db_brand_manual_vector = response.data
        return (
            BrandManualVectorMapper.to_domain(db_brand_manual_vector)
            if db_brand_manual_vector
            else None
        )

    def get_by_brand_id(self, brand_id: str) -> List[BrandManualVectorEntity]:
        logging.info(
            f"Fetching brand manual vectors with brand_id={brand_id}",
            method="get_by_brand_id",
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", brand_id)
            .execute()
        )
        if not response or not response.data:
            return []

        db_brand_manual_vectors = response.data
        return [BrandManualVectorMapper.to_domain(db) for db in db_brand_manual_vectors]

    def list_all(self) -> List[BrandManualVectorEntity]:
        logging.info("Fetching all  ", method="list_all")

        response = self._client.table(self._table).select("*").execute()

        db_brand_manual_vectors = response.data
        return [BrandManualVectorMapper.to_domain(db) for db in db_brand_manual_vectors]
