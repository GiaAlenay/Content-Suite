from dddpy.manual_section.domain.manual_section_entity import ManualSectionEntity
from dddpy.manual_section.infrastructure.manual_section_mapper import (
    ManualSectionMapper,
)
from dddpy.manual_section.domain.manual_section_cmd_repository import (
    ManualSectionCmdRepository,
)

from dddpy.manual_section.domain.manual_section_data import (
    CreateManualSectionData,
    UpdateManualSectionData,
)
from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger
from typing import Optional

logging = Logger("ManualSectionCmdRepositoryImpl")


class ManualSectionCmdRepositoryImpl(ManualSectionCmdRepository):
    def __init__(self):
        self._client = supabase
        self._table = "manual_sections"
        logging.info("ManualSectionCmdRepositoryImpl initialized with Supabase Client")

    async def create(
        self, manual_section: CreateManualSectionData
    ) -> Optional[ManualSectionEntity]:
        logging.info(f"Creating manual_section: {manual_section.brand_id}")

        try:

            data = ManualSectionMapper.to_infrastructure_from_create(manual_section)

            response = await self._client.table(self._table).insert(data).execute()

            if not response.data:
                return None

            db_manual_section = response.data[0]
            logging.info(
                f"ManualSection created successfully with ID: {db_manual_section['id']}",
            )

            return ManualSectionMapper.to_domain(db_manual_section)

        except Exception as e:
            logging.error(f"Error creating manual_section in Supabase: {str(e)}")
            raise e

    async def update(
        self, manual_section_id: str, data: UpdateManualSectionData
    ) -> Optional[ManualSectionEntity]:
        logging.info(f"Updating manual_section with id={manual_section_id}")

        try:
            update_values = ManualSectionMapper.to_infrastructure_from_update(data)

            if not update_values:
                logging.warning("No hay valores para actualizar")
                return {}

            response = (
                self._client.table(self._table)
                .update(update_values)
                .eq("id", manual_section_id)
                .execute()
            )

            logging.info(f"Update success for id={manual_section_id}: {response.data}")
            return response.data

        except Exception as e:
            logging.error(f"Error al actualizar en Supabase: {str(e)}")
            raise e
