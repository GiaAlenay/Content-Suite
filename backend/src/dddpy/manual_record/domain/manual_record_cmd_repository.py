from abc import ABC, abstractmethod
from typing import Optional
from dddpy.manual_record.domain.manual_record_entity import ManualRecordEntity
from dddpy.manual_record.domain.manual_record_data import (
    CreateManualRecordData,
    UpdateManualRecordData,
)


class ManualRecordCmdRepository(ABC):

    @abstractmethod
    async def create(self, manual_record: CreateManualRecordData) -> ManualRecordEntity:
        pass

    @abstractmethod
    async def update(
        self, id: str, manual_record: UpdateManualRecordData
    ) -> Optional[ManualRecordEntity]:
        pass
