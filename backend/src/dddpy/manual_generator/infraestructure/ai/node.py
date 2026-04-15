from langchain_groq import ChatGroq
from .state import ManualState
from dddpy.manual_generator.usecase.manual_generator_schema import AuditManualSchema

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)


async def node_audit(state: ManualState, auditor: AuditAgent):
    """Paso 1: Validar coherencia"""
    report = await auditor.execute(state["brand_description"], state["raw_params"])
    return {
        "audit_report": report.dict(),
        "next_step": "generate" if report.is_coherent else "stop",
    }


async def node_architect(state: ManualState, architect: ArchitectAgent):
    """Paso 2: Redactar contenido completo"""
    content = await architect.execute(state["brand_description"], state["raw_params"])
    return {"full_content": content}


async def node_persist_db(
    state: ManualState,
    repo_version: ManualVersionCmdRepository,
    repo_sections: ManualSectionCmdRepository,
):
    """Paso 3: Persistencia ORM en manual_version y manual_sections"""
    # 1. Crear versión
    version = await repo_version.create(
        state["brand_id"], state["full_content"], state["raw_params"]
    )

    # 2. Fragmentar contenido en secciones (Lógica de dominio)
    sections = split_content_into_sections(state["full_content"])
    for sec in sections:
        await repo_sections.create(version.id, sec.name, sec.content)

    return {"manual_version_id": version.id, "sections": sections}


async def node_vectorize(
    state: ManualState,
    vector_service: VectorizationService,
    repo_vector: BrandManualVectorCmdRepository,
):
    """Paso 4: Vectorización y almacenamiento en brand_manuals_vectors"""
    for sec in state["sections"]:
        # Formato "section_name: texto"
        text_to_embed = f"{sec['name']}: {sec['content']}"
        chunks = vector_service.splitter.split_text(text_to_embed)

        for chunk in chunks:
            vector = await vector_service.to_vectorize_one(chunk)
            await repo_vector.create_one(
                state["manual_version_id"], sec["id"], chunk, vector
            )

    return {"status": "vectorized"}


# --- FLUJO DE CHAT (REFINAMIENTO) ---


async def node_classifier(state: ManualState, classifier: IntentClassifierAgent):
    """Decide si es EDIT o QA"""
    result = await classifier.execute(state["messages"])
    return {"last_intent": result.intent}


async def node_editor(
    state: ManualState, editor: EditorAgent, repo_sections: ManualSectionCmdRepository
):
    """Aplica cambios y actualiza la tabla manual_sections"""
    new_content = await editor.execute(
        state["full_content"], state["messages"][-1].content
    )
    # Aquí el repo actualiza la sección afectada
    await repo_sections.update_full_content(state["manual_version_id"], new_content)
    return {"full_content": new_content}


async def node_qa(
    state: ManualState,
    searcher: SearchAgent,
    vector_service: VectorizationService,
    repo_vector: BrandManualVectorCmdRepository,
    qa_agent: QA_Agent,
):
    """Búsqueda RAG y respuesta"""
    query_opt = await searcher.execute(state["messages"][-1].content, state["messages"])
    vector = await vector_service.to_vectorize_one(query_opt)
    context = await repo_vector.search_similar(state["manual_version_id"], vector)

    answer = await qa_agent.execute(context, state["messages"])
    return {"messages": [("system", answer)]}
