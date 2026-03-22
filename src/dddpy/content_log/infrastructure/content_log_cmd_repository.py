from dddpy.content_log.domain.content_log_entity import ContentLogEntity
from dddpy.content_log.infrastructure.content_log_mapper import ContentLogMapper
from dddpy.content_log.domain.content_log_cmd_repository import ContentLogCmdRepository

from dddpy.content_log.domain.content_log_data import (
    CreateContentLogData,
    UpdateContentLogData,
)
from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger
from typing import Optional

logging = Logger("ContentLogCmdRepositoryImpl")


class ContentLogCmdRepositoryImpl(ContentLogCmdRepository):
    def __init__(self):
        self._client = supabase
        self._table = "content_log"
        logging.info("ContentLogCmdRepositoryImpl initialized with Supabase Client")

    def create(self, content_log: CreateContentLogData) -> Optional[ContentLogEntity]:
        logging.info(f"Creating content_log: {content_log.brand_id}", method="create")

        try:

            data = ContentLogMapper.to_infrastructure_from_create(content_log)

            response = self._client.table(self._table).insert(data).execute()

            if not response.data:
                return None

            db_content_log = response.data[0]
            logging.info(
                f"ContentLog created successfully with ID: {db_content_log['id']}",
                method="create",
            )

            return ContentLogMapper.to_domain(db_content_log)

        except Exception as e:
            logging.error(
                f"Error creating content_log in Supabase: {str(e)}", method="create"
            )
            raise e

    def update(
        self, content_log_id: str, data: UpdateContentLogData
    ) -> Optional[ContentLogEntity]:
        logging.info(f"Updating content_log with id={content_log_id}", method="update")

        try:
            update_values = ContentLogMapper.to_infrastructure_from_update(data)

            if not update_values:
                logging.warning("No hay valores para actualizar", method="update")
                return {}

            response = (
                self._client.table(self._table)
                .update(update_values)
                .eq("id", content_log_id)
                .execute()
            )

            logging.info(f"Update success for id={content_log_id}: {response.data}")
            return response.data

        except Exception as e:
            logging.error(f"Error al actualizar en Supabase: {str(e)}")
            raise e

    def delete(self, content_log_id: str) -> bool:
        logging.info(f"Deleting content_log with id={content_log_id}", method="delete")
        try:
            response = (
                self._client.table(self._table)
                .delete()
                .eq("id", content_log_id)
                .execute()
            )

            success = len(response.data) > 0
            logging.info(
                f"Delete status for id={content_log_id}: {success}", method="delete"
            )
            return success

        except Exception as e:
            logging.error(
                f"Error deleting content_log in Supabase: {str(e)}", method="delete"
            )
            raise e
