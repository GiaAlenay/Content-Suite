from dddpy.content_log.domain.content_log_query_repository import (
    ContentLogQueryRepository,
)
from dddpy.content_log.domain.content_log_entity import ContentLogEntity

from typing import Optional, List


from dddpy.shared.logging.logging import Logger

logging = Logger("ContentLogQueryUseCase")


class ContentLogQueryUseCase:

    def __init__(self, repository: ContentLogQueryRepository):
        logging.info("ContentLogQueryUseCase initialized")
        self.repository = repository

    def get_by_id(self, id: str) -> Optional[ContentLogEntity]:
        logging.info(f"Delegating content_log fetch by id={id}")
        return self.repository.get_by_id(id)

    def get_by_content_log_brand_id(
        self, content_log_brand_id: str
    ) -> List[ContentLogEntity]:
        logging.info(f"Delegating content_log fetch by brand_id={content_log_brand_id}")
        return self.repository.get_by_content_log_brand_id(content_log_brand_id)

    def list_all(self) -> List[ContentLogEntity]:
        logging.info("Delegating content_log list_all")
        return self.repository.list_all()

    def list_by_creator_id(self, creator_id: str) -> List[ContentLogEntity]:
        logging.info("Delegating content_log list_by_creator_id")
        return self.repository.list_by_creator_id(creator_id)
