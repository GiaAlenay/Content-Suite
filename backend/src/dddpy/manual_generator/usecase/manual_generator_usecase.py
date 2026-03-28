from dddpy.shared.logging.logging import Logger
from typing import Dict, Any

logging = Logger("manual_generator_usecase")

from dddpy.brand.domain.brand_exception import BrandNotFound
from dddpy.brand.usecase.brand_query_usecase import (
    BrandQueryUseCase,
)
from dddpy.manual_generator.usecase.manual_architect_agent import BrandArchitectAgent

from dddpy.manual_record.usecase.manual_record_query_usecase import (
    ManualRecordQueryUseCase,
)
from dddpy.manual_record.usecase.manual_record_cmd_usecase import (
    ManualRecordCmdUseCase,
)

from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_usecase import (
    BrandManualVectorCmdUseCase,
)


from dddpy.manual_record.usecase.manual_record_cmd_schema import (
    CreateManualRecordSchema,
    UpdateManualRecordSchema,
)

from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.manual_generator.domain.manual_generator_success import (
    ManualGeneratorSucessMessage,
)

from dddpy.manual_generator.usecase.manual_generator_schema import ManualRequestSchema
from dddpy.manual_generator.usecase.manual_governance_audit_agent import (
    ManualGovernanceAuditor,
)
from dddpy.manual_record.domain.manual_record_exception import ManualRecordNotFound
from dddpy.manual_generator.usecase.manual_generator_pdf import PDFGeneratorService
from dddpy.shared.upload.upload import StorageService
import time


class ManualGeneratorUseCase:
    def __init__(
        self,
        brand_query: BrandQueryUseCase,
        manual_record_cmd: ManualRecordCmdUseCase,
        manual_record_query: ManualRecordQueryUseCase,
        vector_cmd: BrandManualVectorCmdUseCase,
        vectorize_service: VectorizationService,
        brand_architect: BrandArchitectAgent,
        manual_prompt_auditor: ManualGovernanceAuditor,
        pdf_generator: PDFGeneratorService,
        storage: StorageService,
    ):
        logging.info("__init__")
        self.brand_query_usecase = brand_query
        self.manual_record_cmd_usecase = manual_record_cmd
        self.manual_record_query_usecase = manual_record_query
        self.brand_manual_vector_cmd_usecase = vector_cmd
        self.vectorize = vectorize_service
        self.generator = brand_architect
        self.manual_prompt_auditor = manual_prompt_auditor
        self.pdf_generator = pdf_generator
        self.storage = storage
        logging.info("ManualGeneratorUseCase initialized")

    def _get_next_version(self, brand_id: str) -> int:
        current_manual_version = (
            self.manual_record_query_usecase.get_current_version_by_brand_id(brand_id)
        )
        if current_manual_version:
            return current_manual_version.version + 1
        return 1

    def excecute(self, brand_id, raw_parameters: ManualRequestSchema, user_id: str):
        logging.info("exceute")
        logging.info(f"Creating a new manual for brand_id: {brand_id}")
        brand = self.brand_query_usecase.get_by_id(brand_id)
        if not brand or brand.status != "ACTIVE":
            raise BrandNotFound()

        version = 1
        current_manual_version = (
            self.manual_record_query_usecase.get_current_version_by_brand_id(brand_id)
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
            brand_name=brand.name, raw_params=raw_parameters.model_dump()
        )
        to_create_manual_record = CreateManualRecordSchema(
            brand_id=brand_id,
            full_manual=full_manual,
            version=version,
            raw_parameters=raw_parameters.model_dump(),
        )
        new_manual_record = self.manual_record_cmd_usecase.create(
            to_create_manual_record
        )
        to_create_vector_data_list = (
            self.vectorize.prepare_chunks_for_brand_manual_vector(
                manual_id=new_manual_record.id,
                brand_id=brand_id,
                full_manual=full_manual,
                creator_id=user_id,
            )
        )
        self.brand_manual_vector_cmd_usecase.bulk_insert_vectors(
            vector_list=to_create_vector_data_list
        )

        success = ResponseSuccessSchema(
            success=True,
            message=ManualGeneratorSucessMessage.MANUAL_GENERATED,
            data=new_manual_record.to_dict(),
        )
        logging.info(f"Manual Generated successfully: {success}")
        return success

    def audit_and_generate(self, brand_id: str, raw_parameters: ManualRequestSchema):
        brand = self.brand_query_usecase.get_by_id(brand_id)
        audit_report = self.manual_prompt_auditor.verify_manual_params(
            brand.description, raw_parameters.model_dump()
        )
        logging.info(f"audit : {audit_report}")

        if not audit_report["is_coherent"] and audit_report["severity"] == "HIGH":
            return ResponseSuccessSchema(
                success=True,
                message=f"{ManualGeneratorSucessMessage.MANUAL_PROMPT_AUDITED} conflictos de coherencia detectados",
                data=audit_report.model_dump(),
            )

        full_manual = self.generator.generate_human_manual(
            brand_name=brand.name,
            raw_params=raw_parameters.model_dump(),
            brand_description=brand.description,
            audit_feedback=audit_report.feedback,
        )

        new_manual_record = self.manual_record_cmd_usecase.create(
            CreateManualRecordSchema(
                brand_id=brand_id,
                full_manual=full_manual,
                version=self._get_next_version(brand_id),
                raw_parameters=raw_parameters.model_dump(),
                is_current_version=False,
                agent_feedback=audit_report.model_dump(),
            )
        )

        return ResponseSuccessSchema(
            success=True,
            message=ManualGeneratorSucessMessage.MANUAL_DRAFT_GENERATED,
            data=new_manual_record.to_dict(),
        )

    def execute_refinement(self, manual_id: str, refinement_prompt: str):
        previous_manual = self.manual_record_query_usecase.get_by_id(manual_id)
        if not previous_manual:
            raise ManualRecordNotFound()

        brand = self.brand_query_usecase.get_by_id(previous_manual.brand_id)

        audit_context = {
            "original_form_params": previous_manual.raw_parameters,
            "new_refinement_instruction": refinement_prompt,
        }

        refinement_audit = self.manual_prompt_auditor.verify_manual_params(
            brand_description=brand.description, raw_params=audit_context
        )

        if not refinement_audit.is_coherent and refinement_audit.severity == "HIGH":
            return ResponseSuccessSchema(
                success=False,
                message=f"{ManualGeneratorSucessMessage.MANUAL_PROMPT_AUDITED} conflictos de coherencia detectados",
                data=refinement_audit.model_dump(),
            )

        refined_content = self.generator.refine_manual(
            current_content=previous_manual.full_manual,
            refinement_instructions=refinement_prompt,
            brand_name=brand.name,
            audit_feedback=refinement_audit.feedback,
        )

        new_params = previous_manual.raw_parameters
        new_params["last_refinement"] = refinement_prompt

        new_manual_record = self.manual_record_cmd_usecase.create(
            CreateManualRecordSchema(
                brand_id=brand.id,
                full_manual=refined_content,
                version=self._get_next_version(brand.id),
                raw_parameters=new_params,
                is_current_version=False,
                agent_feedback=refinement_audit.model_dump(),
            )
        )

        return ResponseSuccessSchema(
            success=True,
            message=ManualGeneratorSucessMessage.MANUAL_DRAFT_REFINED,
            data=new_manual_record.to_dict(),
        )

    def confirm_manual(self, manual_id: str, user_id: str):
        manual = self.manual_record_query_usecase.get_by_id(manual_id)
        brand = self.brand_query_usecase.get_by_id(manual.brand_id)

        current_manual_version = (
            self.manual_record_query_usecase.get_current_version_by_brand_id(
                manual.brand_id
            )
        )
        if current_manual_version:
            self.manual_record_cmd_usecase.update(
                current_manual_version.id,
                UpdateManualRecordSchema(is_current_version=False),
            )
            self.brand_manual_vector_cmd_usecase.deactivate_by_manual_record_id(
                current_manual_version.id
            )

        to_create_vector_data_list = (
            self.vectorize.prepare_chunks_for_brand_manual_vector(
                manual_id=manual.id,
                brand_id=manual.brand_id,
                full_manual=manual.full_manual,
                creator_id=user_id,
            )
        )
        self.brand_manual_vector_cmd_usecase.bulk_insert_vectors(
            to_create_vector_data_list
        )

        pdf_bytes = self.pdf_generator.create_brand_manual_pdf(
            brand_name=brand.name,
            brand_code=brand.code,
            parameters=manual.raw_parameters,
            content=manual.full_manual,
        )

        unique_name = f"manual_{int(time.time())}.pdf"
        path_on_bucket = f"{brand.code}/manuals/{unique_name}"

        pdf_url = self.storage.upload_file(
            file_bytes=pdf_bytes,
            destination_path=path_on_bucket,
            content_type="application/pdf",
        )

        self.manual_record_cmd_usecase.update(
            manual.id,
            UpdateManualRecordSchema(is_current_version=True, url_manual=pdf_url),
        )

        success = ResponseSuccessSchema(
            success=True,
            message=ManualGeneratorSucessMessage.MANUAL_GENERATED_CONFIRMED,
            data={"url_manual": pdf_url},
        )
        logging.info(f"Manual Generated successfully: {success}")
        return success
