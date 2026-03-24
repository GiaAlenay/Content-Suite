from dddpy.brand.domain.brand_entity import BrandEntity
from dddpy.brand.infrastructure.brand_mapper import BrandMapper
from dddpy.brand.domain.brand_cmd_repository import BrandCmdRepository

from dddpy.brand.domain.brand_data import (
    CreateBrandData,
    UpdateBrandData,
)
from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger
from typing import Optional

logging = Logger("BrandCmdRepositoryImpl")


class BrandCmdRepositoryImpl(BrandCmdRepository):
    def __init__(self):
        self._client = supabase
        self._table = "brands"
        logging.info("BrandCmdRepositoryImpl initialized with Supabase Client")

    def create(self, brand: CreateBrandData) -> Optional[BrandEntity]:
        logging.info(
            f"Creating brand: {brand.name}",
        )

        try:

            data = BrandMapper.to_infrastructure_from_create(brand)
            response = self._client.table(self._table).insert(data).execute()
            if not response or not response.data:
                return None

            db_brand = response.data[0]
            logging.info(
                f"Brand created successfully with ID: {db_brand['id']}",
            )
            return BrandMapper.to_domain(db_brand)

        except Exception as e:
            logging.error(
                f"Error creating brand in Supabase: {str(e)}",
            )
            raise e

    def update(self, brand_id: str, data: UpdateBrandData) -> Optional[BrandEntity]:
        logging.info(
            f"Updating brand with id={brand_id}",
        )
        try:
            update_values = BrandMapper.to_infrastructure_from_update(data)

            if not update_values:
                logging.warning(
                    "No hay valores para actualizar",
                )
                return None
            response = (
                self._client.table(self._table)
                .update(update_values)
                .eq("id", brand_id)
                .execute()
            )
            logging.info(f"Update success for id={brand_id}: {response.data}")
            db_brand = response.data[0]
            logging.info(
                f"Brand updates successfully with ID: {db_brand['id']}",
            )

            mapeado = BrandMapper.to_domain(db_brand)

            return mapeado

        except Exception as e:
            logging.error(f"Error al actualizar en Supabase: {str(e)}")
            raise e

    def delete(self, brand_id: str) -> bool:
        logging.info(
            f"Deleting brand with id={brand_id}",
        )
        try:
            response = (
                self._client.table(self._table).delete().eq("id", brand_id).execute()
            )

            success = len(response.data) > 0
            logging.info(
                f"Delete status for id={brand_id}: {success}",
            )
            return success

        except Exception as e:
            logging.error(
                f"Error deleting brand in Supabase: {str(e)}",
            )
            raise e
