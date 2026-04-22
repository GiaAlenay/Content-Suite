from dddpy.manual_generator.infraestructure.ai.state import ManualState
from dddpy.manual_generator.infraestructure.ai.agents.IntentOrchestratorAgent import (
    IntentOrchestratorAgent,
)

from dddpy.manual_generator.infraestructure.ai.agents.PromptAuditAgent import (
    PromptAuditAgent,
)

from dddpy.manual_generator.infraestructure.ai.agents.ContextDiscoveryAgent import (
    ContextDiscoveryAgent,
)

from dddpy.manual_generator.infraestructure.ai.agents.PromptUpgraderAgent import (
    PromptUpgraderAgent,
)

from langchain_core.messages import AIMessage
from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)


async def node_intent_orchestrator(
    state: ManualState, intent_specify_agent: IntentOrchestratorAgent
):
    # Ejecutamos el agente usando el historial de mensajes que cargó el session_manager
    result = await intent_specify_agent.execute(
        history=state["messages"], brand_description=state["brand_description"]
    )

    # Si es CLARIFY o OUT_OF_SCOPE, añadimos el razonamiento como un mensaje
    # para que el history_logger tenga algo que guardar como respuesta.
    new_messages = []
    if result.tasks[0].task_type in ["CLARIFY", "OUT_OF_SCOPE"]:
        new_messages.append(AIMessage(content=result.tasks[0].description))

    return {
        "planned_tasks": [task.dict() for task in result.tasks],
        "current_task_idx": 0,
        "messages": new_messages,  # Se añade a la lista existente vía 'add'
    }


async def node_chat_audit(state: ManualState, prompt_auditor_agent: PromptAuditAgent):
    # Tomamos el último mensaje del usuario
    user_prompt = state["messages"][-1].content

    # Ejecutamos la auditoría
    audit_result = await prompt_auditor_agent.execute(
        brand_description=state["brand_description"], user_prompt=user_prompt
    )

    # Si el cambio es incoherente, preparamos el mensaje de rechazo
    new_messages = []
    if not audit_result.is_coherent:
        refusal = (
            audit_result.suggested_refusal_message
            or "Lo siento, ese cambio no se alinea con la identidad de tu marca."
        )
        new_messages.append(AIMessage(content=refusal))

    return {
        "chat_audit_report": audit_result.dict(),
        "messages": new_messages,
        # Si no es coherente, el router debería detectar esto para ir a history_logger
        "next_step": "proceed" if audit_result.is_coherent else "block",
    }


async def node_context_retriever(
    state: ManualState,
    context_discovery_agent: ContextDiscoveryAgent,
    vector_query: BrandManualVectorQueryUseCase,  # Tu UseCase para buscar en pgvector
):
    """
    Responsabilidad: Poblar state['retrieved_context'] con la data necesaria.
    """
    # 1. Decidir estrategia
    user_prompt = state["messages"][-1].content
    strategy = await context_discovery_agent.execute(
        user_prompt, state["planned_tasks"]
    )

    context_fragments = []

    # 2. Si es global, traemos el full_content que cargó el session_manager
    if strategy.requires_full_manual:
        context_fragments.append(state["full_content"])
    else:
        # 3. Si es específico, buscamos por vectores
        for query in strategy.search_queries:
            # Buscamos los top 3 fragmentos más similares para esa query
            search_results = await vector_query.search_similar_chunks(
                brand_id=state["brand_id"],
                manual_version_id=state["manual_version_id"],
                query_text=query,
                limit=3,
            )
            for res in search_results:
                context_fragments.append(f"[{res.section_name}]: {res.content_chunk}")

    # Unimos todo en un string de contexto
    final_context = "\n---\n".join(
        set(context_fragments)
    )  # set() para evitar duplicados

    return {"retrieved_context": final_context, "next_step": "proceed"}


async def node_prompt_upgrade(
    state: ManualState, prompt_upgrade_agent: PromptUpgraderAgent
):
    """
    Responsabilidad: Transformar la petición del usuario en una orden técnica.
    """
    # Usamos el último mensaje del usuario y la data recuperada en el nodo anterior
    user_prompt = state["messages"][-1].content

    refined_data = await prompt_upgrade_agent.execute(
        user_prompt=user_prompt,
        brand_description=state["brand_description"],
        retrieved_context=state["retrieved_context"],
    )

    # Guardamos la instrucción refinada en el estado para que el Editor la use
    return {
        "refined_prompt": refined_data.technical_instruction,
        "next_step": "proceed",
    }
