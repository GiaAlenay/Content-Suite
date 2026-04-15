from dddpy.manual_record.domain.manual_record_entity import ManualRecordEntity
from dddpy.manual_record.infrastructure.manual_record_mapper import ManualRecordMapper
from dddpy.manual_record.domain.manual_record_cmd_repository import (
    ManualRecordCmdRepository,
)

from dddpy.manual_record.domain.manual_record_data import (
    CreateManualRecordData,
    UpdateManualRecordData,
)
from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger
from typing import Optional

logging = Logger("ManualRecordCmdRepositoryImpl")


class ManualRecordCmdRepositoryImpl(ManualRecordCmdRepository):
    def __init__(self):
        self._client = supabase
        self._table = "manual_record"
        logging.info("ManualRecordCmdRepositoryImpl initialized with Supabase Client")

    async def create(
        self, manual_record: CreateManualRecordData
    ) -> Optional[ManualRecordEntity]:
        logging.info(f"Creating manual_record: {manual_record.brand_id}")

        try:

            data = ManualRecordMapper.to_infrastructure_from_create(manual_record)

            response = await self._client.table(self._table).insert(data).execute()

            if not response.data:
                return None

            db_manual_record = response.data[0]
            logging.info(
                f"ManualRecord created successfully with ID: {db_manual_record['id']}",
            )

            return ManualRecordMapper.to_domain(db_manual_record)

        except Exception as e:
            logging.error(f"Error creating manual_record in Supabase: {str(e)}")
            raise e

    async def update(
        self, manual_version_id: str, data: UpdateManualRecordData
    ) -> Optional[ManualRecordEntity]:
        logging.info(f"Updating manual_record with id={manual_version_id}")

        try:
            update_values = ManualRecordMapper.to_infrastructure_from_update(data)

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
