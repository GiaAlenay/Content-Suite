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
from typing import Optional

logging = Logger("BrandManualVectorCmdRepositoryImpl")


class BrandManualVectorCmdRepositoryImpl(BrandManualVectorCmdRepository):
    def __init__(self):
        self._client = supabase
        logging.info(
            "BrandManualVectorCmdRepositoryImpl initialized with Supabase Client"
        )

    def create(
        self, brand_manual_vector: CreateBrandManualVectorData
    ) -> BrandManualVectorEntity:
        logging.info(
            f"Creating brand_manual_vector: {brand_manual_vector.brand_id}",
            method="create",
        )

        try:

            data = BrandManualVectorMapper.to_infrastructure_from_create(
                brand_manual_vector
            )

            response = self._client.table(self._table).insert(data).execute()

            if not response.data:
                raise Exception("No se pudo insertar el vector")

            db_brand_manual_vector = response.data[0]
            logging.info(
                f"BrandManualVector created successfully with ID: {db_brand_manual_vector['id']}",
                method="create",
            )

            return BrandManualVectorMapper.to_domain(db_brand_manual_vector)

        except Exception as e:
            logging.error(
                f"Error creating brand_manual_vector in Supabase: {str(e)}",
                method="create",
            )
            raise e

    def update(
        self, brand_manual_vector_id: str, data: UpdateBrandManualVectorData
    ) -> Optional[BrandManualVectorEntity]:
        logging.info(
            f"Updating brand_manual_vector with id={brand_manual_vector_id}",
            method="update",
        )

        try:
            update_values = BrandManualVectorMapper.to_infrastructure_from_update(data)

            if not update_values:
                logging.warning("No hay valores para actualizar", method="update")
                return {}

            response = (
                self._client.table(self._table)
                .update(update_values)
                .eq("id", brand_manual_vector_id)
                .execute()
            )

            logging.info(
                f"Update success for id={brand_manual_vector_id}: {response.data}"
            )
            return response.data

        except Exception as e:
            logging.error(f"Error al actualizar en Supabase: {str(e)}")
            raise e

    def delete(self, brand_manual_vector_id: str) -> bool:
        logging.info(
            f"Deleting brand_manual_vector with id={brand_manual_vector_id}",
            method="delete",
        )
        try:
            response = (
                self._client.table(self._table)
                .delete()
                .eq("id", brand_manual_vector_id)
                .execute()
            )

            success = len(response.data) > 0
            logging.info(
                f"Delete status for id={brand_manual_vector_id}: {success}",
                method="delete",
            )
            return success

        except Exception as e:
            logging.error(
                f"Error deleting brand_manual_vector in Supabase: {str(e)}",
                method="delete",
            )
            raise e
