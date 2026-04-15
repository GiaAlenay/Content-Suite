from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)
from dddpy.brand_manual_vector.infrastructure.brand_manual_vector_mapper import (
    BrandManualVectorMapper,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_cmd_repository import (
    BrandManualVectorCmdRepository,
)

from dddpy.brand_manual_vector.domain.brand_manual_vector_data import (
    CreateBrandManualVectorData,
    UpdateBrandManualVectorData,
)
from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger
from typing import Optional, List
from typing import Dict, Any

logging = Logger("BrandManualVectorCmdRepositoryImpl")


class BrandManualVectorCmdRepositoryImpl(BrandManualVectorCmdRepository):
    def __init__(self):
        self._client = supabase
        self._table = "brand_manuals_vectors"
        logging.info(
            "BrandManualVectorCmdRepositoryImpl initialized with Supabase Client"
        )

    async def create(
        self, brand_manual_vector: CreateBrandManualVectorData
    ) -> Optional[BrandManualVectorEntity]:
        logging.info(f"Creating brand_manual_vector: {brand_manual_vector.brand_id}")

        try:
            data = BrandManualVectorMapper.to_infrastructure_from_create(
                brand_manual_vector
            )
            response = await self._client.table(self._table).insert(data).execute()
            if not response.data:
                return None
            db_brand_manual_vector = response.data[0]
            logging.info(
                f"BrandManualVector created successfully with ID: {db_brand_manual_vector['id']}"
            )
            return BrandManualVectorMapper.to_domain(db_brand_manual_vector)

        except Exception as e:
            logging.error(
                f"Error creating brand_manual_vector in Supabase: {str(e)}",
            )
            raise e

    async def update(
        self, brand_manual_vector_id: str, data: UpdateBrandManualVectorData
    ) -> Optional[BrandManualVectorEntity]:
        logging.info(f"Updating brand_manual_vector with id={brand_manual_vector_id}")

        try:
            update_values = BrandManualVectorMapper.to_infrastructure_from_update(data)
            if not update_values:
                logging.warning("No hay valores para actualizar")
                return None
            response = (
                self._client.table(self._table)
                .update(update_values)
                .eq("id", brand_manual_vector_id)
                .execute()
            )
            logging.info(
                f"Update success for id={brand_manual_vector_id}: {response.data}"
            )
            return BrandManualVectorMapper.to_domain(response.data)

        except Exception as e:
            logging.error(f"Error al actualizar en Supabase: {str(e)}")
            raise e

    async def deactivate_by_manual_version_id(
        self, manual_version_id: str
    ) -> List[Dict[str, Any]]:
        logging.info(
            f"Deactivating all ACTIVE vectors for manual_version_id={manual_version_id}"
        )

        try:
            update_values = {"status": "INACTIVE"}

            response = (
                self._client.table(self._table)
                .update(update_values)
                .eq("manual_version_id", manual_version_id)
                .eq("status", "ACTIVE")
                .execute()
            )

            logging.info(f"Mass update success. Records affected: {len(response.data)}")

            return response.data

        except Exception as e:
            logging.error(
                f"Error al realizar actualización masiva en Supabase: {str(e)}"
            )
            raise e

    async def delete(self, brand_manual_vector_id: str) -> bool:
        logging.info(f"Deleting brand_manual_vector with id={brand_manual_vector_id}")
        try:
            response = (
                self._client.table(self._table)
                .delete()
                .eq("id", brand_manual_vector_id)
                .execute()
            )

            success = len(response.data) > 0
            logging.info(f"Delete status for id={brand_manual_vector_id}: {success}")
            return success

        except Exception as e:
            logging.error(f"Error deleting brand_manual_vector in Supabase: {str(e)}")
            raise e

    async def bulk_insert_vectors(self, vector_list: list[CreateBrandManualVectorData]):

        try:
            data_list = [
                BrandManualVectorMapper.to_infrastructure_from_create(
                    brand_manual_vector
                )
                for brand_manual_vector in vector_list
            ]
            result = await self._client.table(self._table).insert(data_list).execute()
            logging.info(f"Se insertaron {len(vector_list)} fragmentos vectorizados.")
            return result.data
        except Exception as e:
            logging.error(f"Error en inserción masiva: {str(e)}")
            raise e
