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

    async def create(self, brand_manual_vector_data: CreateBrandManualVectorSchema):
        logging.info(f"Delegating brand_manual_vector creation ")
        data = CreateBrandManualVectorData(
            manual_version_id=brand_manual_vector_data.manual_version_id,
            content_chunk=brand_manual_vector_data.content_chunk,
            embedding=brand_manual_vector_data.embedding,
            manual_section_id=brand_manual_vector_data.manual_section_id,
            metadata=brand_manual_vector_data.metadata,
            status=brand_manual_vector_data.status,
        )

        return await self.repository.create(data)

    async def bulk_update_status_by_manual_version_id(
        self, version_id: str, status: str
    ) -> bool:
        logging.info(
            f"Delegating brand_manual_vector bulk_update_status_by_manual_version_id for version_id={version_id}"
        )
        return await self.repository.bulk_update_status_by_manual_version_id(
            version_id=version_id, status=status
        )

    async def update(
        self,
        id: str,
        brand_manual_vector_data: UpdateBrandManualVectorSchema,
    ) -> Optional[BrandManualVectorEntity]:
        logging.info(f"Delegating brand_manual_vector update for id={id}")
        data = UpdateBrandManualVectorData(
            status=brand_manual_vector_data.status,
        )
        return await self.repository.update(id, data)

    async def deactivate_by_manual_version_id(
        self, manual_version_id: str
    ) -> List[Dict[str, Any]]:
        logging.info(
            f"Delegating brand_manual_vector deactivation for manual_version_id={manual_version_id}"
        )
        return await self.repository.deactivate_by_manual_version_id(manual_version_id)

    async def delete(self, id: str) -> bool:
        logging.info(f"Delegating brand_manual_vector delete for id={id}")
        return await self.repository.delete(id)

    async def bulk_insert_vectors(
        self, vector_list: list[CreateBrandManualVectorSchema]
    ):
        logging.info(f"Delegating craetion odbrand_manual_vector list for ")
        data_list = [
            CreateBrandManualVectorData(
                manual_version_id=bmv.manual_version_id,
                content_chunk=bmv.content_chunk,
                embedding=bmv.embedding,
                manual_section_id=bmv.manual_section_id,
                metadata=bmv.metadata,
                status=bmv.status,
            )
            for bmv in vector_list
        ]
        return await self.repository.bulk_insert_vectors(data_list)
