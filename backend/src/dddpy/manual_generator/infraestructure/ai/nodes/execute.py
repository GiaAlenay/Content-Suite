from dddpy.manual_generator.infraestructure.ai.state import ManualState


from dddpy.manual_generator.infraestructure.ai.agents.EditorAgent import EditorAgent
from dddpy.manual_generator.infraestructure.ai.agents.QAAgent import QAAgent

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

from langchain_core.messages import AIMessage


async def node_editor(state: ManualState, editor_agent: EditorAgent):
    """
    Responsabilidad: Generar el nuevo contenido basado en la instrucción técnica.
    """
    # Ejecutamos la edición
    result = await editor_agent.execute(
        brand_description=state["brand_description"],
        retrieved_context=state["retrieved_context"],
        refined_instruction=state["refined_prompt"],
    )

    # 1. Preparamos el mensaje de la IA para el historial de chat
    ai_response = f"{result.explanation_of_changes}\n\nHe actualizado las secciones correspondientes."

    # 2. Lógica de Parcheo (Merging):
    # Si el Editor solo devolvió partes, necesitamos reconstruir el full_content
    # para que persist_db_manuals pueda guardarlo como una nueva versión completa.

    # Por ahora, para simplificar y asegurar coherencia, el Editor suele
    # reconstruir el bloque de contenido que se le pasó.
    new_full_content = "\n\n".join([s.content for s in result.modified_sections])

    # Si el cambio fue local (vía vectores), aquí podrías unirlo al full_content previo
    # Pero lo más seguro es que el editor devuelva el nuevo estado deseado del texto.

    return {
        "full_content": new_full_content,
        "sections": [s.dict() for s in result.modified_sections],
        "messages": [AIMessage(content=ai_response)],
        "next_step": "persist",
    }


async def node_qa(state: ManualState, qa_agent: QAAgent):
    """
    Responsabilidad: Responder consultas sobre el manual actual.
    """
    # Usamos el contexto que ya fue recuperado por 'context_retriever'
    # El retriever ya hizo el trabajo de buscar en los vectores.

    user_question = state["messages"][-1].content

    result = await qa_agent.execute(
        user_question=user_question, retrieved_context=state["retrieved_context"]
    )

    # Formateamos la respuesta para el chat, incluyendo fuentes si existen
    sources_text = (
        f"\n\n*Fuentes: {', '.join(result.sources)}*" if result.sources else ""
    )
    full_response = f"{result.answer}{sources_text}"

    return {
        "messages": [AIMessage(content=full_response)],
        "next_step": "end",  # El flujo de QA termina yendo al history_logger
    }


async def node_approve_manual(
    state: ManualState, manual_version_cmd: ManualVersionCmdUseCase
):
    """
    Responsabilidad: Marcar la versión actual como definitiva.
    """
    version_id = state.get("manual_version_id")

    if not version_id:
        return {
            "messages": [
                AIMessage(content="No encontré una versión activa para aprobar.")
            ],
            "next_step": "end",
        }

    # 1. Actualizamos el estado en la base de datos
    # Esto podría disparar otras acciones, como generar un PDF o enviar un email.
    await manual_version_cmd.update_status(version_id, status="PUBLISHED")

    # 2. Preparamos el mensaje final de éxito
    response = (
        "¡Felicidades! El Manual de Marca ha sido aprobado y guardado como versión final. "
        "Ya puedes descargar el documento o compartirlo."
    )

    return {"messages": [AIMessage(content=response)], "next_step": "end"}


# async def node_approve_manual(
#     state: ManualState,
#     manual_version_cmd: ManualVersionCmdUseCase,
#     vector_cmd: BrandManualVectorCmdUseCase,
# ):
#     version_id = state["manual_version_id"]

#     # 1. Cambiamos estado de la versión
#     await manual_version_cmd.update_status(version_id, status="APPROVED")

#     # 2. Cambiamos estado de los vectores para que el RAG sepa que son oficiales
#     await vector_cmd.update_status_by_version(version_id, status="APPROVED")

#     # 3. Aquí podrías disparar la generación de PDF (un servicio externo)
#     # pdf_url = await pdf_service.generate(state["full_content"])

#     return {
#         "messages": [
#             SystemMessage(content="¡Manual aprobado y publicado oficialmente!")
#         ]
#     }


# ············· sin usar
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


# async def node_persist_chat_history(state: ManualState, chat_cmd: ChatCommandUseCase):
#     last_message = state["messages"][-1]

#     await chat_cmd.save_message(
#         brand_id=state["brand_id"],
#         content=last_message.content,
#         role="USER" if isinstance(last_message, HumanMessage) else "ASSISTANT",
#     )
#     return {}


# async def node_prompt_intention_classifier(
#     state: ManualState, classifier: IntentClassifierAgent
# ):
#     """Decide la intencion del prompt  del usuario"""
#     result = await classifier.execute(state["messages"])
#     return {"last_intent": result.intent}
