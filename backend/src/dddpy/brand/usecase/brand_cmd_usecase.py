from dddpy.brand.usecase.brand_cmd_schema import CreateBrandSchema, UpdateBrandSchema
from dddpy.brand.domain.brand_data import CreateBrandData, UpdateBrandData

from dddpy.brand.domain.brand_cmd_repository import BrandCmdRepository
from dddpy.brand.domain.brand_entity import BrandEntity

from typing import Optional
from dddpy.shared.logging.logging import Logger

logging = Logger("BrandCmdUseCase")


class BrandCmdUseCase:

    def __init__(self, repository: BrandCmdRepository):
        self.repository = repository
        logging.info("BrandCmdUseCase initialized")

    def create(self, brand_data: CreateBrandSchema):
        logging.info(f"Delegating brand creation for code={brand_data.code}")
        data = CreateBrandData(
            code=brand_data.code,
            name=brand_data.name,
            description=brand_data.description,
            logo_url=brand_data.logo_url,
        )

        return self.repository.create(data)

    def update(self, id: str, brand_data: UpdateBrandSchema) -> Optional[BrandEntity]:
        logging.info(f"Delegating brand update for id={id}")
        data = UpdateBrandData(
            name=brand_data.name,
            description=brand_data.description,
            logo_url=brand_data.logo_url,
            status=brand_data.status,
        )
        return self.repository.update(id, data)

    def delete(self, id: str) -> bool:
        logging.info(f"Delegating brand delete for id={id}")
        return self.repository.delete(id)
