from dddpy.manual_record.usecase.manual_record_cmd_schema import (
    CreateManualRecordSchema,
    UpdateManualRecordSchema,
)
from dddpy.manual_record.domain.manual_record_data import (
    CreateManualRecordData,
    UpdateManualRecordData,
)

from dddpy.manual_record.domain.manual_record_cmd_repository import (
    ManualRecordCmdRepository,
)
from dddpy.manual_record.domain.manual_record_entity import ManualRecordEntity

from typing import Optional
from dddpy.shared.logging.logging import Logger

logging = Logger("ManualRecordCmdUseCase")


class ManualRecordCmdUseCase:

    def __init__(self, repository: ManualRecordCmdRepository):
        self.repository = repository
        logging.info("ManualRecordCmdUseCase initialized")

    def create(self, manual_record_data: CreateManualRecordSchema):
        logging.info(
            f"Delegating manual_record creation for brand_id={manual_record_data.brand_id}"
        )
        data = CreateManualRecordData(
            brand_id=manual_record_data.brand_id,
            version=manual_record_data.version,
            full_manual=manual_record_data.full_manual,
            raw_parameters=manual_record_data.raw_parameters,
            is_current_version=manual_record_data.is_current_version,
            url_manual=manual_record_data.url_manual,
            agent_feedback=manual_record_data.agent_feedback,
        )

        return self.repository.create(data)

    def update(
        self, id: str, manual_record_data: UpdateManualRecordSchema
    ) -> Optional[ManualRecordEntity]:
        logging.info(f"Delegating manual_record update for id={id}")
        data = UpdateManualRecordData(
            is_current_version=manual_record_data.is_current_version,
            url_manual=manual_record_data.url_manual,
            agent_feedback=manual_record_data.agent_feedback,
        )
        return self.repository.update(id, data)
