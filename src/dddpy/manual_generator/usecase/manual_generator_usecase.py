from dddpy.shared.logging.logging import Logger
from typing import Dict, Any

logging = Logger("manual_generator_usecase")

from dddpy.brand.domain.brand_exception import BrandNotFound
from dddpy.brand.usecase.brand_query_usecase import (
    BrandQueryUseCase,
)
from dddpy.brand.usecase.brand_factory import brand_query_usecase_factory

from dddpy.manual_record.usecase.manual_record_query_usecase import (
    ManualRecordQueryUseCase,
)
from dddpy.manual_record.usecase.manual_record_cmd_usecase import (
    ManualRecordCmdUseCase,
)
from dddpy.manual_record.usecase.manual_record_factory import (
    manual_record_cmd_usecase_factory,
    manual_record_query_usecase_factory,
)

from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_usecase import (
    BrandManualVectorCmdUseCase,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_factory import (
    brand_manual_vector_cmd_usecase_factory,
    brand_manual_vector_query_usecase_factory,
)


from dddpy.manual_generator.usecase.manual_generador_service import (
    BrandGeneratorService,
)

from dddpy.manual_record.usecase.manual_record_cmd_schema import (
    CreateManualRecordSchema,
    UpdateManualRecordSchema,
)

from dddpy.manual_generator.usecase.vector_service import VectorizationService
from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.manual_generator.domain.manual_generator_success import (
    ManualGeneratorSucessMessage,
)


class ManualGeneratorUseCase:
    def __init__(self):
        logging.info("__init__")
        self.brand_query_usecase: BrandQueryUseCase = brand_query_usecase_factory()
        self.manual_record_cmd_usecase: ManualRecordCmdUseCase = (
            manual_record_cmd_usecase_factory()
        )
        self.manual_record_query_usecase: ManualRecordQueryUseCase = (
            manual_record_query_usecase_factory()
        )
        self.brand_manual_vector_cmd_usecase: BrandManualVectorCmdUseCase = (
            brand_manual_vector_cmd_usecase_factory()
        )
        self.brand_manual_vector_query_usecase: BrandManualVectorQueryUseCase = (
            brand_manual_vector_query_usecase_factory()
        )
        self.generator = BrandGeneratorService()
        self.vectorize = VectorizationService()
        logging.info("ManualGeneratorUseCase initialized")

    def excecute(self, brand_id, raw_parameters: Dict[str, Any]):
        logging.info("exceute")
        logging.info(f"Creating a new manual for brand_id: {brand_id}")
        brand = self.brand_query_usecase.get_by_id(brand_id)
        if not brand or brand.status != "ACTIVE":
            raise BrandNotFound()

        version = 1
        current_manual_version = (
            self.manual_record_query_usecase.get_latest_version_by_brand_id(brand_id)
        )
        if current_manual_version:
            version = current_manual_version.version + 1
            self.manual_record_cmd_usecase.update(
                current_manual_version.id,
                UpdateManualRecordSchema(is_current_version=False),
            )
            self.brand_manual_vector_cmd_usecase.deactivate_by_manual_record_id(
                current_manual_version.id
            )

        full_manual = self.generator.generate_human_manual(
            brand_name=brand.name, raw_params=raw_parameters
        )
        to_create_manual_record = CreateManualRecordSchema(
            brand_id=brand_id,
            full_manual=full_manual,
            version=version,
            raw_parameters=raw_parameters,
        )
        new_manual_record = self.manual_record_cmd_usecase.create(
            to_create_manual_record
        )
        vector_data_list = self.vectorize.prepare_chunks_for_db(
            manual_id=new_manual_record.id,
            brand_id=brand_id,
            full_manual=full_manual,
            creator_id="e125dc69-eb45-4af8-8343-57092522f3fe",
        )
        self.brand_manual_vector_cmd_usecase.bulk_insert_vectors(
            vector_list=vector_data_list
        )

        success = ResponseSuccessSchema(
            success=True,
            message=ManualGeneratorSucessMessage.MANUAL_GENERATED,
            data=new_manual_record.to_dict(),
        )
        logging.info(f"Manual Generated successfully: {success}")
        return success
