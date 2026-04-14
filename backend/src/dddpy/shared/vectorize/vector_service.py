from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_schema import (
    CreateBrandManualVectorSchema,
)

from dddpy.content_log.usecase.content_log_cmd_schema import CreateContentLogSchema
import os
from dotenv import load_dotenv

load_dotenv()


class VectorizationService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key,
            task_type="retrieval_document",
            output_dimensionality=768,
        )
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=60)

    async def prepare_chunks_for_brand_manual_vector(
        self, manual_id: str, brand_id: str, full_manual: str, creator_id: str
    ):
        chunks = await self.splitter.split_text(full_manual)
        vector_items = []

        vectors = await self.embeddings.embed_documents(chunks)

        for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
            vector_items.append(
                CreateBrandManualVectorSchema(
                    brand_id=brand_id,
                    manual_record_id=manual_id,
                    content_chunk=chunk,
                    embedding=vector,
                    metadata={"chunk_index": i, "total_chunks": len(chunks)},
                    creator_id=creator_id,
                )
            )

        return vector_items

    async def to_vectorize_one(self, prompt_origin: str):
        return self.embeddings.embed_query(prompt_origin)
