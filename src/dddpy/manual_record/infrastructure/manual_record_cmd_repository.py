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
        logging.info("ManualRecordCmdRepositoryImpl initialized with Supabase Client")

    def create(self, manual_record: CreateManualRecordData) -> ManualRecordEntity:
        logging.info(
            f"Creating manual_record: {manual_record.brand_id}", method="create"
        )

        try:

            data = ManualRecordMapper.to_infrastructure_from_create(manual_record)

            response = self._client.table(self._table).insert(data).execute()

            if not response.data:
                raise Exception("No se pudo insertar la marca")

            db_manual_record = response.data[0]
            logging.info(
                f"ManualRecord created successfully with ID: {db_manual_record['id']}",
                method="create",
            )

            return ManualRecordMapper.to_domain(db_manual_record)

        except Exception as e:
            logging.error(
                f"Error creating manual_record in Supabase: {str(e)}", method="create"
            )
            raise e
