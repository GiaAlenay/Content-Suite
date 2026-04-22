from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_schema import (
    CreateBrandManualVectorSchema,
    UpdateBrandManualVectorSchema,
)
from dddpy.manual_section.usecase.manual_section_cmd_schema import (
    CreateManualSectionSchema,
)
from dddpy.manual_version.usecase.manual_version_cmd_schema import (
    CreateManualVersionSchema,
    UpdateManualVersionSchema,
)

from dddpy.manual_section.usecase.manual_section_cmd_usecase import (
    ManualSectionCmdUseCase,
)

from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_usecase import (
    BrandManualVectorCmdUseCase,
)

from dddpy.manual_generator.domain.manual_parser import split_content_into_sections
from dddpy.manual_generator.infraestructure.ai.state import ManualState
from dddpy.manual_version.usecase.manual_version_cmd_usecase import (
    ManualVersionCmdUseCase,
)
from dddpy.manual_version.usecase.manual_version_query_usecase import (
    ManualVersionQueryUseCase,
)

from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.chat_history.usecase.chat_history_query_usecase import (
    ChatHistoryQueryUseCase,
)
from dddpy.chat_history.usecase.chat_history_cmd_usecase import ChatHistoryCmdUseCase

from dddpy.chat_session.usecase.chat_session_query_usecase import (
    ChatSessionQueryUseCase,
)


async def node_session_manager(
    state: ManualState,
    chat_session_query: ChatSessionQueryUseCase,
    manual_version_query: ManualVersionQueryUseCase,
):
    """
    Responsabilidad: Inicializar el estado del chat.
    Recupera historial y la última versión del manual para que los agentes
    tengan contexto de 'sobre qué' están hablando.
    """
    brand_id = state["brand_id"]

    # 1. Buscar o crear sesión de chat
    session = await chat_session_query.get_or_create_active_session(brand_id)

    # 2. Recuperar historial (últimos 15 mensajes para la ventana de contexto)
    history = await chat_session_query.get_recent_history(session.id, limit=15)

    # 3. Recuperar la versión actual del manual para tener el full_content
    current_version = await manual_version_query.get_current_version_by_brand_id(
        brand_id
    )

    # Convertimos el historial de la DB a mensajes de LangChain
    chat_messages = []
    for msg in history:
        if msg.role == "USER":
            chat_messages.append(HumanMessage(content=msg.content))
        else:
            chat_messages.append(AIMessage(content=msg.content))

    return {
        "chat_session_id": session.id,
        "manual_version_id": current_version.id if current_version else None,
        "full_content": current_version.full_content if current_version else None,
        "messages": chat_messages,  # El 'add' del TypedDict los unirá al prompt actual
    }


async def node_history_logger(
    state: ManualState,
    chat_history_cmd: ChatHistoryCmdUseCase,
    vector_service: VectorizationService,  # Para el embedding de la columna nueva
):
    """
    Responsabilidad: Persistir el intercambio final.
    Guarda el USER prompt y la respuesta SYSTEM/AI con sus embeddings.
    """
    # Tomamos el último mensaje (IA) y el anterior (Usuario)
    user_msg = state["messages"][-2].content
    ai_msg = state["messages"][-1].content

    # Generamos embeddings para la búsqueda semántica futura en el historial
    user_vector = await vector_service.to_vectorize(user_msg)
    ai_vector = await vector_service.to_vectorize(ai_msg)

    # Guardado en DB
    await chat_history_cmd.save_message(
        session_id=state["chat_session_id"],
        content=user_msg,
        role="USER",
        embedding=user_vector,
    )

    await chat_history_cmd.save_message(
        session_id=state["chat_session_id"],
        content=ai_msg,
        role="ASSISTANT",
        embedding=ai_vector,
        manual_version_id=state.get(
            "manual_version_id"
        ),  # Link a la versión que generó
    )

    return {"messages": []}  # No necesitamos retornar nada más


async def node_persist_db_manuals(
    state: ManualState,
    manual_version_cmd: ManualVersionCmdUseCase,
    manual_version_query: ManualVersionQueryUseCase,
    manual_sections_cmd: ManualSectionCmdUseCase,
):
    """Editado: Ahora maneja incremento de versiones tanto en Gen como en Edit"""

    # Obtenemos el número de versión anterior
    old_version_data = await manual_version_query.get_current_version_by_brand_id(
        state["brand_id"]
    )
    new_version_number = (
        (old_version_data.version_number + 1) if old_version_data else 1
    )

    # Si estamos en CHAT (Edit), usamos los raw_params que ya tenía el manual anterior
    # si es que no se pasaron nuevos parámetros.
    current_params = state.get("raw_params") or (
        old_version_data.raw_parameters if old_version_data else {}
    )

    to_create_manual_version = CreateManualVersionSchema(
        brand_id=state["brand_id"],
        version_number=new_version_number,
        full_content=state["full_content"],
        raw_parameters=current_params,
        status="DRAFT",
    )

    version = await manual_version_cmd.create(to_create_manual_version)

    # El split_content_into_sections debe ser robusto para Markdown
    sections = split_content_into_sections(state["full_content"])
    to_create_sections = [
        CreateManualSectionSchema(
            manual_version_id=version.id,
            section_name=sec["section_name"],
            content=sec["content"],
            order_number=sec["order_number"],
        )
        for sec in sections
    ]

    new_sections_entities = await manual_sections_cmd.bulk_insert(to_create_sections)
    new_sections_data = [sec.to_dict() for sec in new_sections_entities]

    return {
        "manual_version_id": version.id,
        "sections": new_sections_data,
        "raw_params": current_params,  # Aseguramos que los params viajen en el estado
    }


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
