import os
from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

# from langgraph.checkpoint.postgres import AsyncPostgresSaver

from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")


pool = AsyncConnectionPool(conninfo=DB_URL, max_size=20, min_size=1)


try:
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    print("Importación exitosa de AsyncPostgresSaver")
except ImportError:
    try:
        # Intento alternativo para versiones específicas
        from langgraph_checkpoint_postgres.aio import AsyncPostgresSaver

        print("Importación exitosa con guion bajo")
    except ImportError as e:
        print(f"No se pudo encontrar el módulo. Error: {e}")


@asynccontextmanager
async def get_db_checkpointer():
    """
    Manager asíncrono para obtener el checkpointer de LangGraph.
    """
    async with pool.connection() as conn:
        checkpointer = AsyncPostgresSaver(conn)

        await checkpointer.setup()

        yield checkpointer
