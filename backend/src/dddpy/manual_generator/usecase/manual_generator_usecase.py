from dddpy.shared.logging.logging import Logger
from typing import Dict, Any, Optional

logging = Logger("manual_generator_usecase")

from dddpy.brand.domain.brand_exception import BrandNotFound
from dddpy.brand.usecase.brand_query_usecase import (
    BrandQueryUseCase,
)

from dddpy.manual_version.domain.manual_version_exception import ManualVersionNotFound
from dddpy.manual_version.usecase.manual_version_query_usecase import (
    ManualVersionQueryUseCase,
)
from dddpy.manual_version.usecase.manual_version_cmd_usecase import (
    ManualVersionCmdUseCase,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.manual_generator.domain.manual_generator_success import (
    ManualGeneratorSucessMessage,
)

from langchain_core.messages import HumanMessage


class ManualGeneratorUseCase:
    def __init__(
        self,
        graph_builder,
        brand_query: BrandQueryUseCase,
        manual_version_cmd: ManualVersionCmdUseCase,
        manual_version_query: ManualVersionQueryUseCase,
    ):
        logging.info("__init__")
        self.graph_builder = graph_builder
        self.brand_query = brand_query
        self.manual_version_cmd = manual_version_cmd
        self.manual_version_query = manual_version_query

        logging.info("ManualGeneratorUseCase initialized")

    async def initialize_generation(self, brand_id: str, params: dict):

        brand = await self.brand_query.get_by_id(brand_id)
        if not brand or brand.status != "ACTIVE":
            raise BrandNotFound()

        config = {"configurable": {"thread_id": brand_id}}

        initial_state = {
            "brand_name": brand.name,
            "brand_code": brand.code,
            "brand_id": brand_id,
            "brand_description": brand.description,
            "raw_params": params,
            "messages": [],
        }

        final_state = await self.graph_builder.ainvoke(initial_state, config)

        return ResponseSuccessSchema(
            success=True,
            message=ManualGeneratorSucessMessage.MANUAL_DRAFT_GENERATED,
            data={
                "manual_version_id": final_state.get("manual_version_id"),
                "full_content": final_state.get("full_content"),
                "audit_report": final_state.get("audit_report"),
            },
        )

    async def process_chat_interaction(self, brand_id: str, message: str):
        current_version = (
            await self.manual_version_query.get_current_version_by_brand_id(brand_id)
        )

        if not current_version:
            raise ManualVersionNotFound()

        config = {"configurable": {"thread_id": brand_id}}

        initial_state = {
            "brand_id": brand_id,
            "manual_version_id": current_version["id"],
            "full_content": current_version["full_content"],
            "messages": [HumanMessage(content=message)],
        }

        final_state = await self.graph_builder.ainvoke(
            initial_state, config, start_node="session_manager"
        )

        return ResponseSuccessSchema(
            success=True,
            message=ManualGeneratorSucessMessage.MANUAL_DRAFT_REFINED,
            data={
                "answer": final_state["messages"][-1].content,
                "intent": final_state.get("last_intent"),
                "new_version_id": final_state.get("manual_version_id"),
            },
        )

    async def approve_and_finalize(self, brand_id: str):

        config = {"configurable": {"thread_id": brand_id}}
        initial_state = await self.graph_builder.get_state(config)
        version_id = initial_state.values.get("manual_version_id")

        if not version_id:
            raise Exception("No active version found to approve")

        final_state = await self.graph_builder.ainvoke(
            initial_state, config, start_node="approve_manual"
        )

        return ResponseSuccessSchema(
            success=True,
            message=ManualGeneratorSucessMessage.MANUAL_GENERATED_CONFIRMED,
            data={"pdf_url": final_state.get("pdf_url")},
        )

    # async def _get_next_version(self, brand_id: str) -> int:
    #     current_manual_version = (
    #         self.manual_record_query_usecase.get_current_version_by_brand_id(brand_id)
    #     )
    #     if current_manual_version:
    #         return current_manual_version.version + 1
    #     return 1

    # async def excecute(
    #     self, brand_id, raw_parameters: ManualRequestSchema, user_id: str
    # ):
    #     logging.info("exceute")
    #     logging.info(f"Creating a new manual for brand_id: {brand_id}")
    #     brand = await self.brand_query_usecase.get_by_id(brand_id)
    #     if not brand or brand.status != "ACTIVE":
    #         raise BrandNotFound()

    #     version = 1
    #     current_manual_version = (
    #         self.manual_record_query_usecase.get_current_version_by_brand_id(brand_id)
    #     )
    #     if current_manual_version:
    #         version = current_manual_version.version + 1
    #         self.manual_record_cmd_usecase.update(
    #             current_manual_version.id,
    #             UpdateManualRecordSchema(is_current_version=False),
    #         )
    #         self.brand_manual_vector_cmd_usecase.deactivate_by_manual_version_id(
    #             current_manual_version.id
    #         )

    #     full_manual = await self.generator.generate_human_manual(
    #         brand_name=brand.name, raw_params=raw_parameters.model_dump()
    #     )
    #     to_create_manual_record = CreateManualRecordSchema(
    #         brand_id=brand_id,
    #         full_manual=full_manual,
    #         version=version,
    #         raw_parameters=raw_parameters.model_dump(),
    #     )
    #     new_manual_record = await self.manual_record_cmd_usecase.create(
    #         to_create_manual_record
    #     )
    #     to_create_vector_data_list = (
    #         self.vectorize.prepare_chunks_for_brand_manual_vector(
    #             manual_id=new_manual_record.id,
    #             brand_id=brand_id,
    #             full_manual=full_manual,
    #             creator_id=user_id,
    #         )
    #     )
    #     self.brand_manual_vector_cmd_usecase.bulk_insert_vectors(
    #         vector_list=to_create_vector_data_list
    #     )

    #     success = ResponseSuccessSchema(
    #         success=True,
    #         message=ManualGeneratorSucessMessage.MANUAL_GENERATED,
    #         data=new_manual_record.to_dict(),
    #     )
    #     logging.info(f"Manual Generated successfully: {success}")
    #     return success

    # async def audit_and_generate(
    #     self, brand_id: str, raw_parameters: ManualRequestSchema
    # ):
    #     brand = await self.brand_query_usecase.get_by_id(brand_id)
    #     audit_report = await self.manual_prompt_auditor.verify_manual_params(
    #         brand.description, raw_parameters.model_dump()
    #     )
    #     logging.info(f"audit : {audit_report}")

    #     if not audit_report["is_coherent"] and audit_report["severity"] == "HIGH":
    #         return ResponseSuccessSchema(
    #             success=True,
    #             message=f"{ManualGeneratorSucessMessage.MANUAL_PROMPT_AUDITED} conflictos de coherencia detectados",
    #             data=audit_report,
    #         )

    #     full_manual = await self.generator.generate_human_manual(
    #         brand_name=brand.name,
    #         raw_params=raw_parameters.model_dump(),
    #         brand_description=brand.description,
    #         audit_feedback=audit_report["feedback"],
    #     )

    #     new_manual_record = await self.manual_record_cmd_usecase.create(
    #         CreateManualRecordSchema(
    #             brand_id=brand_id,
    #             full_manual=full_manual,
    #             version=self._get_next_version(brand_id),
    #             raw_parameters=raw_parameters.model_dump(),
    #             is_current_version=False,
    #             agent_feedback=audit_report,
    #         )
    #     )

    #     return ResponseSuccessSchema(
    #         success=True,
    #         message=ManualGeneratorSucessMessage.MANUAL_DRAFT_GENERATED,
    #         data=new_manual_record.to_dict(),
    #     )

    # async def execute_refinement(self, manual_id: str, refinement_prompt: str):
    #     previous_manual = await self.manual_record_query_usecase.get_by_id(manual_id)
    #     if not previous_manual:
    #         raise ManualRecordNotFound()

    #     brand = await self.brand_query_usecase.get_by_id(previous_manual.brand_id)

    #     audit_context = {
    #         "original_form_params": previous_manual.raw_parameters,
    #         "new_refinement_instruction": refinement_prompt,
    #     }

    #     refinement_audit = await self.manual_prompt_auditor.verify_manual_params(
    #         brand_description=brand.description, raw_params=audit_context
    #     )

    #     if not refinement_audit.is_coherent and refinement_audit.severity == "HIGH":
    #         return ResponseSuccessSchema(
    #             success=True,
    #             message=f"{ManualGeneratorSucessMessage.MANUAL_PROMPT_AUDITED} conflictos de coherencia detectados",
    #             data=refinement_audit,
    #         )

    #     refined_content = await self.generator.refine_manual(
    #         current_content=previous_manual.full_manual,
    #         refinement_instructions=refinement_prompt,
    #         brand_name=brand.name,
    #         audit_feedback=refinement_audit["feedback"],
    #     )

    #     new_params = previous_manual.raw_parameters
    #     new_params["last_refinement"] = refinement_prompt

    #     new_manual_record = await self.manual_record_cmd_usecase.create(
    #         CreateManualRecordSchema(
    #             brand_id=brand.id,
    #             full_manual=refined_content,
    #             version=self._get_next_version(brand.id),
    #             raw_parameters=new_params,
    #             is_current_version=False,
    #             agent_feedback=refinement_audit,
    #         )
    #     )

    #     return ResponseSuccessSchema(
    #         success=True,
    #         message=ManualGeneratorSucessMessage.MANUAL_DRAFT_REFINED,
    #         data=new_manual_record.to_dict(),
    #     )

    # async def confirm_manual(self, manual_id: str, user_id: str):
    #     manual = await self.manual_record_query_usecase.get_by_id(manual_id)
    #     brand = await self.brand_query_usecase.get_by_id(manual.brand_id)

    #     current_manual_version = (
    #         self.manual_record_query_usecase.get_current_version_by_brand_id(
    #             manual.brand_id
    #         )
    #     )
    #     if current_manual_version:
    #         self.manual_record_cmd_usecase.update(
    #             current_manual_version.id,
    #             UpdateManualRecordSchema(is_current_version=False),
    #         )
    #         self.brand_manual_vector_cmd_usecase.deactivate_by_manual_version_id(
    #             current_manual_version.id
    #         )

    #     to_create_vector_data_list = (
    #         self.vectorize.prepare_chunks_for_brand_manual_vector(
    #             manual_id=manual.id,
    #             brand_id=manual.brand_id,
    #             full_manual=manual.full_manual,
    #             creator_id=user_id,
    #         )
    #     )
    #     self.brand_manual_vector_cmd_usecase.bulk_insert_vectors(
    #         to_create_vector_data_list
    #     )

    #     pdf_bytes = await self.pdf_generator.create_brand_manual_pdf(
    #         brand_name=brand.name,
    #         brand_code=brand.code,
    #         parameters=manual.raw_parameters,
    #         content=manual.full_manual,
    #     )

    #     unique_name = f"manual_{int(time.time())}.pdf"

    #     path_on_bucket = f"{brand.code}/manuals/{unique_name}"

    #     pdf_url = await self.storage.upload_file(
    #         file_bytes=pdf_bytes,
    #         destination_path=path_on_bucket,
    #         content_type="application/pdf",
    #     )

    #     print("pdf_url")
    #     print(pdf_url)

    #     self.manual_record_cmd_usecase.update(
    #         manual.id,
    #         UpdateManualRecordSchema(is_current_version=True, url_manual=pdf_url),
    #     )

    #     success = ResponseSuccessSchema(
    #         success=True,
    #         message=ManualGeneratorSucessMessage.MANUAL_GENERATED_CONFIRMED,
    #         data={"url_manual": pdf_url},
    #     )
    #     logging.info(f"Manual Generated successfully: {success}")
    #     return success
