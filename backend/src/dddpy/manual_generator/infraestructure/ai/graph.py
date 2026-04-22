from langgraph.graph import StateGraph, END
from dddpy.manual_generator.infraestructure.ai.state import ManualState
from dddpy.manual_generator.infraestructure.ai.nodes.execute import (
    node_editor,
    node_qa,
    node_approve_manual,
)

from dddpy.manual_generator.infraestructure.ai.nodes.infraestructure_data import (
    node_persist_db_manuals,
    node_vectorize_manual,
    node_session_manager,
    node_history_logger,
)

from dddpy.manual_generator.infraestructure.ai.nodes.first_generate import (
    node_params_audit,
    node_architect,
)

from dddpy.manual_generator.infraestructure.ai.nodes.core import (
    node_intent_orchestrator,
    node_chat_audit,
    node_context_retriever,
    node_prompt_upgrade,
)

from functools import partial


def create_manual_graph(
    checkpointer,
    architect_agent,
    context_discovery_agent,
    editor_agent,
    intent_specify_agent,
    params_auditor_agent,
    prompt_auditor_agent,
    prompt_upgrade_agent,
    qa_agent,
    vectorize_service,
    pdf_generator_service,
    storage_service,
    manual_version_cmd,
    manual_version_query,
    manual_section_cmd,
    brand_manual_vector_cmd,
    chat_session_cmd,
    chat_session_query,
    chat_history_cmd,
    chat_history_query,
):
    workflow = StateGraph(ManualState)

    # --- NODOS DE INFRAESTRUCTURA Y DATOS ---
    workflow.add_node(
        "session_manager",
        partial(
            node_session_manager,
            chat_session_query=chat_session_query,
            manual_version_query=manual_version_query,
        ),
    )  # Carga historial y recupera última versión
    workflow.add_node(
        "persist_db_manuals",
        partial(
            node_persist_db_manuals,
            manual_version_cmd=manual_version_cmd,
            manual_version_query=manual_version_query,
            manual_sections_cmd=manual_section_cmd,
        ),
    )
    workflow.add_node(
        "vectorize_manual",
        partial(
            node_vectorize_manual,
            vectorize_service=vectorize_service,
            brand_manual_vector_cmd=brand_manual_vector_cmd,
        ),
    )  # Crea embeddings del manual
    workflow.add_node(
        "history_logger",
        partial(
            node_history_logger,
            chat_history_cmd=chat_history_cmd,
            vectorize_service=vectorize_service,
        ),
    )  # Persiste el chat (USER + AI) en DB

    # --- NODOS DE GENERACIÓN INICIAL (PUNTO 1) ---
    workflow.add_node(
        "params_auditor",
        partial(node_params_audit, params_auditor_agent=params_auditor_agent),
    )
    workflow.add_node(
        "architect", partial(node_architect, architect_agent=architect_agent)
    )

    # --- NODOS DE INTELIGENCIA DE CHAT (PUNTO 2) ---
    workflow.add_node(
        "orchestrator",
        partial(node_intent_orchestrator, intent_specify_agent=intent_specify_agent),
    )  # El nuevo clasificador multi-tarea
    workflow.add_node(
        "chat_auditor",
        partial(node_chat_audit, prompt_auditor_agent=prompt_auditor_agent),
    )  # Audita la coherencia del pedido
    workflow.add_node(
        "context_retriever",
        partial(
            node_context_retriever, context_discovery_agent=context_discovery_agent
        ),
    )  # Busca fragmentos relevantes
    workflow.add_node(
        "upgrade_prompt",
        partial(node_prompt_upgrade, prompt_upgrade_agent=prompt_upgrade_agent),
    )  # Refina el pedido para el editor

    # --- NODOS DE EJECUCIÓN ---
    workflow.add_node("editor", partial(node_editor, editor_agent=editor_agent))
    workflow.add_node("qa_handler", partial(node_qa, qa_agent=qa_agent))
    workflow.add_node(
        "approve_manual",
        partial(
            node_approve_manual,
            manual_version_cmd=manual_version_cmd,
            pdf_generator_service=pdf_generator_service,
            storage_service=storage_service,
            brand_manual_vector_cmd=brand_manual_vector_cmd,
        ),
    )

    # ==========================================
    # FLUJO 1: GENERACIÓN INICIAL (ENTRY POINT A)
    # ==========================================
    workflow.set_entry_point("params_auditor")

    workflow.add_conditional_edges(
        "params_auditor", lambda x: "architect" if x["next_step"] == "generate" else END
    )
    workflow.add_edge("architect", "persist_db_manuals")
    workflow.add_edge("persist_db_manuals", "vectorize_manual")

    # El Punto 1 termina aquí si no hay chat
    workflow.add_conditional_edges(
        "vectorize_manual",
        lambda x: "history_logger" if x.get("chat_session_id") else END,
    )

    # ==========================================
    # FLUJO 2: CHAT INTERACTION (ENTRY POINT B - vía UseCase)
    # ==========================================
    # El UseCase llama al grafo con start_node="session_manager"
    workflow.add_edge("session_manager", "orchestrator")

    workflow.add_conditional_edges(
        "orchestrator", router_by_task  # Función lógica para decidir el camino
    )

    # Camino A: CLARIFY / UNKNOWN / OUT_OF_SCOPE
    # Salta directo a la respuesta humana sin tocar el manual
    workflow.add_edge("orchestrator", "history_logger")

    workflow.add_conditional_edges(
        "chat_auditor",
        lambda x: (
            "context_retriever" if x["next_step"] == "proceed" else "history_logger"
        ),
    )

    workflow.add_edge("context_retriever", "upgrade_prompt")
    workflow.add_edge("upgrade_prompt", "editor")
    workflow.add_edge("editor", "persist_db_manuals")
    # De persist_db_manuals va a vectorize_manual y de ahí a history_logger por el condicional previo.

    # Camino C: QA
    workflow.add_edge("qa_handler", "history_logger")

    # Camino D: APPROVE
    workflow.add_edge("approve_manual", END)

    # Cierre de ciclo: El logger guarda en DB y termina la interacción
    workflow.add_edge("history_logger", END)

    return workflow.compile(checkpointer=checkpointer)


def router_by_task(state: ManualState):
    """
    Decide a dónde ir basándose en la primera tarea del plan.
    """
    tasks = state.get("planned_tasks", [])
    if not tasks:
        return END

    first_task = tasks[0]["task_type"]

    if first_task == "EDIT":
        return "chat_auditor"

    if first_task == "QA":
        return "qa_handler"

    if first_task == "APPROVE":
        return "approve_manual"

    return "history_logger"


# def create_manual_graph0(
#     checkpointer,
#     params_auditor,
#     architect,
#     classifier,
#     editor,
#     searcher,
#     vectorize_service,
#     manual_version_cmd,
#     manual_version_query,
#     manual_section_cmd,
#     brand_manual_vector_cmd,
# ):
#     workflow = StateGraph(ManualState)

#     workflow.add_node(
#         "params_auditor", partial(node_params_audit, params_auditor=params_auditor)
#     )
#     workflow.add_node("architect", partial(node_architect, architect=architect))
#     workflow.add_node(
#         "persist_db_manuals",
#         partial(
#             node_persist_db_manuals,
#             manual_version_cmd=manual_version_cmd,
#             manual_version_query=manual_version_query,
#             manual_sections_cmd=manual_section_cmd,
#         ),
#     )
#     workflow.add_node(
#         "vectorize_manual",
#         partial(
#             node_vectorize_manual,
#             service=vectorize_service,
#             brand_manual_vector_cmd=brand_manual_vector_cmd,
#         ),
#     )
#     workflow.add_node(
#         "classifier", partial(node_prompt_intention_classifier, classifier=classifier)
#     )
#     workflow.add_node("editor", partial(node_editor, editor=editor))
#     workflow.add_node(
#         "qa_handler", partial(node_qa, searcher=searcher, qa_agent=architect)
#     )

#     workflow.add_node("upgrade_prompt", node_prompt_upgrade)
#     workflow.add_node("persist_chat", node_persist_chat_history)
#     workflow.add_node("approve_manual", node_approve_manual)

#     workflow.set_entry_point("params_auditor")
#     workflow.add_conditional_edges(
#         "params_auditor", lambda x: "architect" if x["next_step"] == "generate" else END
#     )
#     workflow.add_edge("architect", "persist_db_manuals")
#     workflow.add_edge("persist_db_manuals", "vectorize_manual")

#     workflow.add_conditional_edges(
#         "vectorize_manual",
#         lambda x: "persist_chat" if x.get("chat_session_id") else END
#     )

#     workflow.add_edge("vectorize_manual", END)


#     workflow.add_conditional_edges(
#         "classifier",
#         lambda x: {
#             "EDIT": "upgrade_prompt",
#             "QA": "qa_handler",
#             "RESTORE": "restore",
#             "APPROVE": "approve_manual"
#         }.get(x["last_intent"], END)
#     )

#     workflow.add_edge("upgrade_prompt", "editor")
#     workflow.add_edge("editor", "persist_db_manuals")
#     workflow.add_edge("restore", "persist_db_manuals")

#     workflow.add_edge("qa_handler", "persist_chat")
#     workflow.add_edge("approve_manual", END)


#     workflow.add_edge("persist_chat", END)

#     return workflow.compile(checkpointer=checkpointer)
