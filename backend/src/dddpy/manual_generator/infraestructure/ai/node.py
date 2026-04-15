from dddpy.manual_generator.infraestructure.ai.state import ManualState
from dddpy.manual_generator.infraestructure.ai.agents.ParamsAuditAgent import (
    ParamsAuditAgent,
)
from dddpy.manual_generator.infraestructure.ai.agents.ArchitectAgent import (
    ArchitectAgent,
)
from dddpy.manual_generator.infraestructure.ai.agents.RetrievalAgent import SearchAgent
from dddpy.manual_generator.infraestructure.ai.agents.IntentClassifierAgent import (
    IntentClassifierAgent,
)
from dddpy.manual_generator.infraestructure.ai.agents.EditorAgent import EditorAgent

from dddpy.manual_version.usecase.manual_version_cmd_usecase import (
    ManualVersionCmdUseCase,
)
from dddpy.manual_version.usecase.manual_version_query_usecase import (
    ManualVersionQueryUseCase,
)
from dddpy.manual_section.usecase.manual_section_cmd_usecase import (
    ManualSectionCmdUseCase,
)

from dddpy.manual_section.usecase.manual_section_query_usecase import (
    ManualSectionQueryUseCase,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_usecase import (
    BrandManualVectorCmdUseCase,
)
from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.manual_version.usecase.manual_version_cmd_schema import (
    CreateManualVersionSchema,
    UpdateManualVersionSchema,
)

from dddpy.manual_generator.domain.manual_parser import split_content_into_sections
from dddpy.manual_section.usecase.manual_section_cmd_schema import (
    CreateManualSectionSchema,
)
import asyncio
from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_schema import (
    CreateBrandManualVectorSchema,
    UpdateBrandManualVectorSchema,
)


async def node_params_audit(state: ManualState, auditor: ParamsAuditAgent):
    report = await auditor.execute(state["brand_description"], state["raw_params"])

    return {
        "audit_report": report.dict(),
        "next_step": (
            "generate" if report.is_coherent and report.severity != "HIGH" else "stop"
        ),
        "messages": [("assistant", report.human_message)],
    }


async def node_architect(state: ManualState, architect: ArchitectAgent):
    """Paso 2: Redactar contenido compdel manual"""
    content = await architect.execute(
        brand_name=state["brand_name"],
        brand_description=state["brand_description"],
        raw_params=state["raw_params"],
    )
    return {"full_content": content}


async def node_persist_db_manuals(
    state: ManualState,
    manual_version_cmd: ManualVersionCmdUseCase,
    manual_version_query: ManualVersionQueryUseCase,
    manual_sections_cmd: ManualSectionCmdUseCase,
):
    """Guarda el nuevo manual generado en sus tablas"""
    old_manual_version = await manual_version_query.get_current_version_by_brand_id()
    old_version = 0
    if old_manual_version and old_manual_version["version_number"]:
        old_version = old_manual_version["version_number"]

    to_create_manual_version = CreateManualVersionSchema(
        brand_id=state["brand_id"],
        version_number=old_version + 1,
        full_content=state["full_content"],
        raw_parameters=state["raw_params"],
        status="DRAFT",
    )

    version = await manual_version_cmd.create(to_create_manual_version)

    sections = split_content_into_sections(state["full_content"])
    to_create_sections = []
    for sec in sections:
        to_create_sections.append(
            CreateManualSectionSchema(
                manual_version_id=version.id,
                section_name=sec["section_name"],
                content=sec["content"],
                order_number=sec["order_number"],
            )
        )

    new_sections_entities = await manual_sections_cmd.bulk_insert(to_create_sections)

    new_sections_data = [sec.to_dict() for sec in new_sections_entities]

    return {"manual_version_id": version.id, "sections": new_sections_data}


async def node_vectorize_manual(
    state: ManualState,
    vector_service: VectorizationService,
    brand_manual_vector_cmd: BrandManualVectorCmdUseCase,
):
    """Vectoriza el contenido del manual y lo guarda"""

    all_chunks_data = []

    for sec in state["sections"]:

        chunks = vector_service.splitter.split_text(sec["content"])
        for chunk in chunks:
            format_chunk = f"{sec['section_name']}: {chunk}"
            all_chunks_data.append(
                {"format_chunk": format_chunk, "section_id": sec["id"]}
            )

    texts_to_embed = [item["format_chunk"] for item in all_chunks_data]
    vectors = await vector_service.to_vectorize_many(texts_to_embed)

    to_vectorize_schemas = []
    for i, vector in enumerate(vectors):
        to_vectorize_schemas.append(
            CreateBrandManualVectorSchema(
                manual_version_id=state["manual_version_id"],
                content_chunk=all_chunks_data[i]["format_chunk"],
                embedding=vector,
                manual_section_id=all_chunks_data[i]["section_id"],
                status="DRAFT",
            )
        )

    await brand_manual_vector_cmd.bulk_insert_vectors(to_vectorize_schemas)

    return {"status": "vectorized"}


async def node_prompt_intention_classifier(
    state: ManualState, classifier: IntentClassifierAgent
):
    """Decide la intencion del prompt  del usuario"""
    result = await classifier.execute(state["messages"])
    return {"last_intent": result.intent}


async def node_editor(
    state: ManualState, editor: EditorAgent, repo_sections: ManualSectionCmdUseCase
):
    """Aplica cambios y actualiza la tabla manual_sections"""
    new_content = await editor.execute(
        state["full_content"], state["messages"][-1].content
    )

    await repo_sections.update_full_content(state["manual_version_id"], new_content)
    return {"full_content": new_content}


async def node_qa(
    state: ManualState,
    searcher: SearchAgent,
    vector_service: VectorizationService,
    repo_vector: BrandManualVectorCmdUseCase,
    qa_agent: QA_Agent,
):
    """Búsqueda RAG y respuesta"""
    query_opt = await searcher.execute(state["messages"][-1].content, state["messages"])
    vector = await vector_service.to_vectorize_one(query_opt)
    context = await repo_vector.search_similar(state["manual_version_id"], vector)

    answer = await qa_agent.execute(context, state["messages"])
    return {"messages": [("system", answer)]}


async def node_restore_version(
    state: ManualState,
    version_query: ManualVersionQueryUseCase,
    section_query: ManualSectionQueryUseCase,
):
    """
    Busca la versión anterior (o una específica si el usuario la menciona)
    y sobreescribe el estado actual.
    """
    brand_id = state["brand_id"]

    # Lógica: Obtener la penúltima versión o la anterior a la actual
    # Esto depende de cómo implementes tu query, pero básicamente:
    previous_version = await version_query.get_previous_version(brand_id)

    if not previous_version:
        return {
            "messages": [("system", "No encontré una versión anterior para restaurar.")]
        }

    # Recuperar las secciones de esa versión
    old_sections = await section_query.get_by_version_id(previous_version.id)

    return {
        "full_content": previous_version.full_content,
        "manual_version_id": previous_version.id,
        "sections": [sec.to_dict() for sec in old_sections],
        "messages": [
            (
                "system",
                f"Se ha restaurado el manual a la versión {previous_version.version_number}.",
            )
        ],
    }


async def node_report_error(state: ManualState):
    """
    Prepara el reporte de errores para ser devuelto por la API
    cuando la auditoría es HIGH riesgo.
    """
    report = state["audit_report"]

    return {
        "status": "REJECTED",
        "messages": [("system", f"Generación cancelada: {report['summary']}")],
    }
