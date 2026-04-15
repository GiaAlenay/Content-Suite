from langchain_core.prompts import ChatPromptTemplate


class ArchitectAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Eres un Director Creativo de Branding. Genera un manual de marca profesional.
            Estructura el contenido en secciones claras (Misión, Visión, Tonalidad, etc.).
            Usa Markdown. Cada sección debe ser extensa y detallada.""",
                ),
                (
                    "user",
                    "Contexto de Marca: {brand_desc}\nParámetros de este Manual: {params}",
                ),
            ]
        )

    async def execute(self, brand_desc: str, params: dict) -> str:
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"brand_desc": brand_desc, "params": params})
        return response.content
