from langchain_core.prompts import ChatPromptTemplate


class EditorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Eres un Editor Editorial. Tu tarea es modificar secciones del manual de marca basándote en el feedback del usuario, manteniendo la consistencia del resto del documento.",
                ),
                (
                    "user",
                    "CONTENIDO ACTUAL: {content}\n\nSOLICITUD DE CAMBIO: {instruction}",
                ),
            ]
        )

    async def execute(self, current_content: str, instruction: str) -> str:
        chain = self.prompt | self.llm
        response = await chain.ainvoke(
            {"content": current_content, "instruction": instruction}
        )
        return response.content
