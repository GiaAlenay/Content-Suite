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

from typing import Optional, List, Dict, Any
from dddpy.shared.logging.logging import Logger

logging = Logger("BrandManualVectorCmdUseCase")


class BrandManualVectorCmdUseCase:

    def __init__(self, repository: BrandManualVectorCmdRepository):
        self.repository = repository
        logging.info("BrandManualVectorCmdUseCase initialized")

    def create(self, brand_manual_vector_data: CreateBrandManualVectorSchema):
        logging.info(f"Delegating brand_manual_vector creation ")
        data = CreateBrandManualVectorData(
            brand_id=brand_manual_vector_data.brand_id,
            content_chunk=brand_manual_vector_data.content_chunk,
            embedding=brand_manual_vector_data.embedding,
            creator_id=brand_manual_vector_data.creator_id,
            metadata=brand_manual_vector_data.metadata,
            manual_record_id=brand_manual_vector_data.manual_record_id,
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

    def deactivate_by_manual_record_id(
        self, manual_record_id: str
    ) -> List[Dict[str, Any]]:
        logging.info(
            f"Delegating brand_manual_vector deactivation for manual_record_id={manual_record_id}"
        )
        return self.repository.deactivate_by_manual_record_id(manual_record_id)

    def delete(self, id: str) -> bool:
        logging.info(f"Delegating brand_manual_vector delete for id={id}")
        return self.repository.delete(id)

    def bulk_insert_vectors(self, vector_list: list[CreateBrandManualVectorSchema]):
        logging.info(f"Delegating craetion odbrand_manual_vector list for ")
        data_list = [
            CreateBrandManualVectorData(
                brand_id=bmv.brand_id,
                content_chunk=bmv.content_chunk,
                embedding=bmv.embedding,
                creator_id=bmv.creator_id,
                metadata=bmv.metadata,
                manual_record_id=bmv.manual_record_id,
            )
            for bmv in vector_list
        ]
        return self.repository.bulk_insert_vectors(data_list)
