from typing import Optional, List
from dddpy.brand.domain.brand_entity import BrandEntity
from dddpy.brand.domain.brand_query_repository import BrandQueryRepository
from dddpy.brand.infrastructure.brand_mapper import BrandMapper

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("BrandQueryRepositoryImpl")


class BrandQueryRepositoryImpl(BrandQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "brands"
        logging.info("BrandQueryRepositoryImpl initialized with Supabase")

    def get_by_id(self, id: str) -> Optional[BrandEntity]:
        logging.info(f"Fetching brand with id={id}")
        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        print("response by id brand")
        print(response)
        if not response or not response.data:
            return None

        db_brand = response.data
        return BrandMapper.to_domain(db_brand) if db_brand else None

    def get_by_code(self, code: str) -> Optional[BrandEntity]:
        logging.info(f"Fetching brand with code={code}")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("code", code)
            .maybe_single()
            .execute()
        )

        if not response or not response.data:
            return None

        db_brand = response.data
        return BrandMapper.to_domain(db_brand) if db_brand else None

    def get_by_brand_name(self, brand_name: str) -> Optional[BrandEntity]:
        logging.info(f"Fetching brand with brand_name={brand_name}")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("name", brand_name)
            .maybe_single()
            .execute()
        )

        if not response or not response.data:
            return None

        db_brand = response.data
        return BrandMapper.to_domain(db_brand) if db_brand else None

    def list_all(self) -> List[BrandEntity]:
        logging.info("Fetching all brands with current manual URL")

        response = (
            self._client.table(self._table)
            .select("*, manual_record(url_manual)")
            .eq("manual_record.is_current_version", True)
            .order("created_at", desc=True)
            .execute()
        )

        db_brands = response.data
        return [BrandMapper.to_domain(db) for db in db_brands]

    def list_active_with_current_manual(self) -> List[BrandEntity]:
        logging.info("Fetching active brands with current manual")

        response = (
            self._client.table(self._table)
            .select("*, manual_record!inner(*)")
            .eq("status", "ACTIVE")
            .eq("manual_record.is_current_version", True)
            .order("created_at", desc=True)
            .execute()
        )

        db_brands = response.data
        return [BrandMapper.to_domain(db) for db in db_brands]
