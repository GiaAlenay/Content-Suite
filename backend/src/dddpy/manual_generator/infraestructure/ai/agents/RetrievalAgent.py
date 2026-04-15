from langchain_core.prompts import ChatPromptTemplate


class SearchAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Eres un experto en recuperación de información (RAG). Convierte la duda del usuario en una 'Search Query' optimizada para buscar en fragmentos vectoriales de un manual de marca.",
                ),
                ("user", "Duda del usuario: {query}\nHistorial reciente: {history}"),
            ]
        )

    async def execute(self, query: str, history: list) -> str:
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"query": query, "history": history})
        return response.content
