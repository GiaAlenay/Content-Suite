from typing import Optional, List
from dddpy.brand.domain.brand_entity import BrandEntity
from dddpy.brand.domain.brand_query_repository import BrandQueryRepository
from dddpy.brand.infrastructure.brand_mapper import BrandMapper

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("BrandCmdRepositoryImpl")


class BrandQueryRepositoryImpl(BrandQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "companies_companies"
        logging.info("BrandQueryRepositoryImpl initialized with Supabase")

    def get_by_id(self, id: int) -> Optional[BrandEntity]:
        logging.info(f"Fetching brand with id={id}", method="get_by_id")

        # .select("*") es como SELECT *
        # .eq("id", id) es como WHERE id = id
        # .maybe_single() es ideal para traer 1 o nada (evita excepciones si no existe)
        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )

        db_brand = response.data
        return BrandMapper.to_domain(db_brand) if db_brand else None

    def get_by_code(self, code: str) -> Optional[BrandEntity]:
        logging.info(f"Fetching brand with code={code}", method="get_by_code")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("code", code)
            .maybe_single()
            .execute()
        )

        db_brand = response.data
        return BrandMapper.to_domain(db_brand) if db_brand else None

    def get_by_brand_name(self, brand_name: str) -> Optional[BrandEntity]:
        logging.info(
            f"Fetching brand with brand_name={brand_name}", method="get_by_brand_name"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("name", brand_name)
            .maybe_single()
            .execute()
        )

        db_brand = response.data
        return BrandMapper.to_domain(db_brand) if db_brand else None

    def list_all(self) -> List[BrandEntity]:
        logging.info("Fetching all companies", method="list_all")

        response = self._client.table(self._table).select("*").execute()

        db_brands = response.data  # response.data es una lista de diccionarios
        return [BrandMapper.to_domain(db) for db in db_brands]
