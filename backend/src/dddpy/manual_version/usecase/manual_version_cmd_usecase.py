from dddpy.manual_version.usecase.manual_version_cmd_schema import (
    CreateManualVersionSchema,
    UpdateManualVersionSchema,
)
from dddpy.manual_version.domain.manual_version_data import (
    CreateManualVersionData,
    UpdateManualVersionData,
)

from dddpy.manual_version.domain.manual_version_cmd_repository import (
    ManualVersionCmdRepository,
)
from dddpy.manual_version.domain.manual_version_entity import ManualVersionEntity

from typing import Optional
from dddpy.shared.logging.logging import Logger

logging = Logger("ManualVersionCmdUseCase")


class ManualVersionCmdUseCase:

    def __init__(self, repository: ManualVersionCmdRepository):
        self.repository = repository
        logging.info("ManualVersionCmdUseCase initialized")

    def create(self, manual_version_data: CreateManualVersionSchema):
        logging.info(
            f"Delegating manual_version creation for brand_id={manual_version_data.brand_id}"
        )
        data = CreateManualVersionData(
            brand_id=manual_version_data.brand_id,
            version=manual_version_data.version,
            full_manual=manual_version_data.full_manual,
            raw_parameters=manual_version_data.raw_parameters,
            is_current_version=manual_version_data.is_current_version,
            url_manual=manual_version_data.url_manual,
            agent_feedback=manual_version_data.agent_feedback,
        )

        return self.repository.create(data)

    def update(
        self, id: str, manual_version_data: UpdateManualVersionSchema
    ) -> Optional[ManualVersionEntity]:
        logging.info(f"Delegating manual_version update for id={id}")
        data = UpdateManualVersionData(
            is_current_version=manual_version_data.is_current_version,
            url_manual=manual_version_data.url_manual,
            agent_feedback=manual_version_data.agent_feedback,
        )
        return self.repository.update(id, data)
