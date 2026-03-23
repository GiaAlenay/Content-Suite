from abc import ABC, abstractmethod
from typing import Optional, List

from dddpy.content_log.domain.content_log_entity import ContentLogEntity


class ContentLogQueryRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[ContentLogEntity]:
        pass

    @abstractmethod
    def get_by_content_log_brand_id(
        self, content_log_brand_id: str
    ) -> List[ContentLogEntity]:
        pass

    @abstractmethod
    def list_all(self) -> List[ContentLogEntity]:
        pass
