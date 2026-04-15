import os
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver  # Nota el .aio
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")


pool = AsyncConnectionPool(conninfo=DB_URL, max_size=20, min_size=1)


@asynccontextmanager
async def get_db_checkpointer():
    """
    Manager asíncrono para obtener el checkpointer de LangGraph.
    """
    async with pool.connection() as conn:
        checkpointer = AsyncPostgresSaver(conn)

        await checkpointer.setup()

        yield checkpointer
