from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_usecase import (
    BrandManualVectorCmdUseCase,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_factory import (
    brand_manual_vector_cmd_usecase_factory,
    brand_manual_vector_query_usecase_factory,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_schema import (
    CreateBrandManualVectorSchema,
    UpdateBrandManualVectorSchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("brand_manual_vector_usecase")

from dddpy.brand_manual_vector.domain.brand_manual_vector_exception import (
    BrandManualVectorNotFound,
)
from dddpy.brand_manual_vector.domain.brand_manual_vector_success import (
    BrandManualVectorSucessMessage,
)


class BrandManualVectorUseCase:
    def __init__(self):
        logging.info("__init__")
        self.brand_manual_vector_cmd_usecase: BrandManualVectorCmdUseCase = (
            brand_manual_vector_cmd_usecase_factory()
        )
        self.brand_manual_vector_query_usecase: BrandManualVectorQueryUseCase = (
            brand_manual_vector_query_usecase_factory()
        )
        logging.info("BrandManualVectorUseCase initialized")

    def create(self, brand_manual_vector_data: CreateBrandManualVectorSchema):
        logging.info("create")
        logging.info(
            f"Creating a new brand_manual_vector with data: {brand_manual_vector_data}"
        )

        new_brand_manual_vector = self.brand_manual_vector_cmd_usecase.create(
            brand_manual_vector_data
        )
        success = ResponseSuccessSchema(
            success=True,
            message=BrandManualVectorSucessMessage.BRANDMANUALVECTOR_CREATED,
            data=new_brand_manual_vector.to_dict(),
        )
        logging.info(f"BrandManualVector created successfully: {success}")
        return success

    def get_by_id(self, id: str):
        logging.info("get_by_id")
        brand_manual_vector = self.brand_manual_vector_query_usecase.get_by_id(id)
        if not brand_manual_vector:
            raise BrandManualVectorNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=BrandManualVectorSucessMessage.BRANDMANUALVECTOR_GET,
            data=brand_manual_vector.to_dict(),
        )
        logging.info(f"BrandManualVector retrieved successfully by id={id}")
        return success

    def get_by_brand_id(self, brand_id: str):
        logging.info("get_by_brand_id")
        brand_manual_vector = self.brand_manual_vector_query_usecase.get_by_brand_id(
            brand_id
        )
        if not brand_manual_vector:
            raise BrandManualVectorNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=BrandManualVectorSucessMessage.BRANDMANUALVECTOR_GET,
            data=brand_manual_vector.to_dict(),
        )
        logging.info(f"BrandManualVector retrieved successfully by brand_id={brand_id}")
        return success

    def update(
        self,
        id: str,
        brand_manual_vector_data: UpdateBrandManualVectorSchema,
    ):
        logging.info("update")
        logging.info(
            f"Updating brand_manual_vector {id} with data: {brand_manual_vector_data}"
        )
        updated_brand_manual_vector = self.brand_manual_vector_cmd_usecase.update(
            id, brand_manual_vector_data
        )
        if not updated_brand_manual_vector:
            raise BrandManualVectorNotFound()

        success = ResponseSuccessSchema(
            success=True,
            message=BrandManualVectorSucessMessage.BRANDMANUALVECTOR_UPDATED,
            data=updated_brand_manual_vector.to_dict(),
        )
        logging.info(f"BrandManualVector updated successfully: {success}")
        return success

    def delete_by_brand_id(self, brand_id: str):
        logging.info("delete_by_brand_id")
        logging.info(f"Deleting brand_manual_vectors by brand_id= {brand_id}")

        deleted = self.brand_manual_vector_cmd_usecase.delete(brand_id)
        if not deleted:
            raise BrandManualVectorNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=BrandManualVectorSucessMessage.BRANDMANUALVECTOR_DELETED,
            data={},
        )
        logging.info(f"BrandManualVector deleted successfully: {success}")
        return success

    def list_all(self):
        logging.info("list_all")
        brand_manual_vector = self.brand_manual_vector_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=BrandManualVectorSucessMessage.BRANDMANUALVECTORS_GET,
            data=[c.to_dict() for c in brand_manual_vector],
        )
        logging.info(
            f"BrandManualVectors listed successfully: {len(brand_manual_vector)} brand_manual_vector"
        )
        return success
