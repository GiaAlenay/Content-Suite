from functools import wraps
from langfuse import observe, get_client
from dddpy.auth.context import current_user_ctx
import asyncio


def audit_trace(name: str):
    async def decorator(func):
        @observe(name=name)
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_data = current_user_ctx.get()
            langfuse = get_client()

            langfuse.update_current_trace(user_id=user_data.get("email"))
            langfuse.update_current_span(
                metadata={"brand": kwargs.get("brand_name", "N/A")}
            )

            if asyncio.iscoroutinefunction(func):
                return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
