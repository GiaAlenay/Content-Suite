from langgraph.graph import StateGraph, END
from dddpy.manual_generator.infraestructure.ai.state import ManualState
from dddpy.manual_generator.infraestructure.ai.node import (
    node_audit,
    node_architect,
    node_persist_db,
    node_vectorize,
    node_classifier,
    node_editor,
    node_qa,
)

from functools import partial


def create_manual_graph(
    checkpointer,
    auditor,
    architect,
    classifier,
    editor,
    searcher,
    vectorize_service,
    manual_record_cmd,
    vector_cmd,
):
    workflow = StateGraph(ManualState)

    # Registro de Nodos
    workflow.add_node("auditor", partial(node_audit, auditor=auditor))
    workflow.add_node("architect", partial(node_architect, architect=architect))
    workflow.add_node("persist_db", partial(node_persist_db, repo=manual_record_cmd))
    workflow.add_node(
        "vectorize", partial(node_vectorize, service=vectorize_service, repo=vector_cmd)
    )
    workflow.add_node("classifier", partial(node_classifier, classifier=classifier))
    workflow.add_node("editor", partial(node_editor, editor=editor))
    workflow.add_node(
        "qa_handler", partial(node_qa, searcher=searcher, qa_agent=architect)
    )

    # --- LÓGICA DE BORDES (EDGES) ---

    workflow.set_entry_point("auditor")

    # Decisión después de auditar
    workflow.add_conditional_edges(
        "auditor", lambda x: "architect" if x["next_step"] == "generate" else END
    )

    workflow.add_edge("architect", "persist_db")
    workflow.add_edge("persist_db", "vectorize")

    # Después de vectorizar, el grafo se PAUSA.
    # Si el usuario vuelve por el endpoint de chat, despertará en el 'classifier'.
    workflow.add_edge("vectorize", END)

    # Punto de entrada para el Chat
    workflow.add_conditional_edges(
        "classifier", lambda x: "editor" if x["last_intent"] == "EDIT" else "qa_handler"
    )

    # Si se edita, volvemos a vectorizar para mantener sincronía
    workflow.add_edge("editor", "vectorize")
    workflow.add_edge("qa_handler", END)

    return workflow.compile(checkpointer=checkpointer)
