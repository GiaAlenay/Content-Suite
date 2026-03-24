from dddpy.brand.usecase.brand_cmd_usecase import BrandCmdUseCase
from dddpy.brand.usecase.brand_query_usecase import BrandQueryUseCase
from dddpy.brand.usecase.brand_factory import (
    brand_cmd_usecase_factory,
    brand_query_usecase_factory,
)
from dddpy.brand.usecase.brand_cmd_schema import (
    CreateBrandSchema,
    UpdateBrandSchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("brand_usecase")

from dddpy.brand.domain.brand_exception import (
    BrandNotFound,
    RepeatedBrandCode,
)
from dddpy.brand.domain.brand_success import BrandSucessMessage


class BrandUseCase:
    def __init__(self):
        logging.info("__init__")
        self.brand_cmd_usecase: BrandCmdUseCase = brand_cmd_usecase_factory()
        self.brand_query_usecase: BrandQueryUseCase = brand_query_usecase_factory()
        logging.info("BrandUseCase initialized")

    def create(self, brand_data: CreateBrandSchema):
        print("estoy en create brand")
        logging.info("create")
        logging.info(f"Creating a new brand with data: {brand_data}")

        existing_code = self.brand_query_usecase.get_by_code(brand_data.code)

        if existing_code:
            raise RepeatedBrandCode()

        new_brand = self.brand_cmd_usecase.create(brand_data)
        success = ResponseSuccessSchema(
            success=True,
            message=BrandSucessMessage.BRAND_CREATED,
            data=new_brand.to_dict(),
        )
        logging.info(f"Brand created successfully: {success}")
        return success

    def get_by_id(self, id: str):
        logging.info("get_by_id")
        brand = self.brand_query_usecase.get_by_id(id)
        if not brand or brand.status != "ACTIVE":
            raise BrandNotFound()
        success = ResponseSuccessSchema(
            success=True, message=BrandSucessMessage.BRAND_GET, data=brand.to_dict()
        )
        logging.info(f"Brand retrieved successfully by id={id}")
        return success

    def get_by_code(self, code: str):
        logging.info("get_by_code")
        brand = self.brand_query_usecase.get_by_code(code)
        if not brand or brand.status != "ACTIVE":
            raise BrandNotFound()
        success = ResponseSuccessSchema(
            success=True, message=BrandSucessMessage.BRAND_GET, data=brand.to_dict()
        )
        logging.info(f"Brand retrieved successfully by id={id}")
        return success

    def get_by_brand_name(self, brand_name: str):
        logging.info("get_by_code")
        brand = self.brand_query_usecase.get_by_brand_name(brand_name)
        if not brand or brand.status != "ACTIVE":
            raise BrandNotFound()
        success = ResponseSuccessSchema(
            success=True, message=BrandSucessMessage.BRAND_GET, data=brand.to_dict()
        )
        logging.info(f"Brand retrieved successfully by name={brand_name}")
        return success

    def update(self, id: str, brand_data: UpdateBrandSchema):
        logging.info("update")
        logging.info(f"Updating brand {id} with data: {brand_data}")

        brand = self.brand_query_usecase.get_by_id(id)
        if not brand:
            raise BrandNotFound()

        updated_brand = self.brand_cmd_usecase.update(id, brand_data)

        success = ResponseSuccessSchema(
            success=True,
            message=BrandSucessMessage.BRAND_UPDATED,
            data=updated_brand.to_dict() if updated_brand else None,
        )
        logging.info(f"Brand updated successfully: {success}")
        return success

    def delete(self, id: str):
        logging.info("delete")
        logging.info(f"Deleting brand {id}")

        deleted = self.brand_cmd_usecase.delete(id)
        if not deleted:
            raise BrandNotFound()
        success = ResponseSuccessSchema(
            success=True, message=BrandSucessMessage.BRAND_DELETED, data={}
        )
        logging.info(f"Brand deleted successfully: {success}")
        return success

    def list_all(self):
        logging.info("list_all")
        brand = self.brand_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=BrandSucessMessage.BRANDS_GET,
            data=[c.to_dict() for c in brand],
        )
        logging.info(f"Brands listed successfully: {len(brand)} brand")
        return success
