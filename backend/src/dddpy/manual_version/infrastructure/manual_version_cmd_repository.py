from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity
from dddpy.manual_version.infrastructure.manual_version_mapper import (
    ManualVersionMapper,
)
from dddpy.manual_version.domain.manual_version_cmd_repository import (
    ManualVersionCmdRepository,
)

from dddpy.manual_version.domain.manual_version_data import (
    CreateManualVersionData,
    UpdateManualVersionData,
)
from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger
from typing import Optional

logging = Logger("ManualVersionCmdRepositoryImpl")


class ManualVersionCmdRepositoryImpl(ManualVersionCmdRepository):
    def __init__(self):
        self._client = supabase
        self._table = "manual_version"
        logging.info("ManualVersionCmdRepositoryImpl initialized with Supabase Client")

    async def create(
        self, manual_version: CreateManualVersionData
    ) -> Optional[ManualVersionEntity]:
        logging.info(f"Creating manual_version: {manual_version.brand_id}")

        try:

            data = ManualVersionMapper.to_infrastructure_from_create(manual_version)

            response = await self._client.table(self._table).insert(data).execute()

            if not response.data:
                return None

            db_manual_version = response.data[0]
            logging.info(
                f"ManualVersion created successfully with ID: {db_manual_version['id']}",
            )

            return ManualVersionMapper.to_domain(db_manual_version)

        except Exception as e:
            logging.error(f"Error creating manual_version in Supabase: {str(e)}")
            raise e

    async def update(
        self, manual_version_id: str, data: UpdateManualVersionData
    ) -> Optional[ManualVersionEntity]:
        logging.info(f"Updating manual_version with id={manual_version_id}")

        try:
            update_values = ManualVersionMapper.to_infrastructure_from_update(data)

            if not update_values:
                logging.warning("No hay valores para actualizar")
                return {}

            response = (
                self._client.table(self._table)
                .update(update_values)
                .eq("id", manual_version_id)
                .execute()
            )

            logging.info(f"Update success for id={manual_version_id}: {response.data}")
            return response.data

        except Exception as e:
            logging.error(f"Error al actualizar en Supabase: {str(e)}")
            raise e

    async def update_status_and_pdf(
        self, id: str, status: str, url_pdf: Optional[str] = None
    ):
        """Para el nodo de Aprobación Final"""
        update_data = {"status": status}
        if url_pdf:
            update_data["url_pdf_manual"] = url_pdf

        await self._client.table(self._table).update(update_data).eq("id", id).execute()
