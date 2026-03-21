from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_schema import (
    CreateBrandManualVectorSchema,
    UpdateBrandManualVectorSchema,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_data import (
    CreateBrandManualVectorData,
    UpdateBrandManualVectorData,
)

from dddpy.brand_manual_vector.domain.brand_manual_vector_cmd_repository import (
    BrandManualVectorCmdRepository,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_entity import (
    BrandManualVectorEntity,
)

from typing import Optional
from dddpy.shared.logging.logging import Logger

logging = Logger("BrandManualVectorCmdUseCase")


class BrandManualVectorCmdUseCase:

    def __init__(self, repository: BrandManualVectorCmdRepository):
        self.repository = repository
        logging.info("BrandManualVectorCmdUseCase initialized")

    def create(self, brand_manual_vector_data: CreateBrandManualVectorSchema):
        logging.info(
            f"Delegating brand_manual_vector creation for code={brand_manual_vector_data.code}"
        )
        data = CreateBrandManualVectorData(
            brand_id=brand_manual_vector_data.brand_id,
            content_chunk=brand_manual_vector_data.content_chunk,
            embedding=brand_manual_vector_data.embedding,
            creator_id=brand_manual_vector_data.creator_id,
            metadata=brand_manual_vector_data.metadata,
        )

        return self.repository.create(data)

    def update(
        self,
        id: str,
        brand_manual_vector_data: UpdateBrandManualVectorSchema,
    ) -> Optional[BrandManualVectorEntity]:
        logging.info(f"Delegating brand_manual_vector update for id={id}")
        data = UpdateBrandManualVectorData(
            status=brand_manual_vector_data.status,
        )
        return self.repository.update(id, data)

    def delete(self, id: str) -> bool:
        logging.info(f"Delegating brand_manual_vector delete for id={id}")
        return self.repository.delete(id)
