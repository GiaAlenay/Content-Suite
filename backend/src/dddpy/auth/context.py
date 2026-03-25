from contextvars import ContextVar


current_user_ctx: ContextVar[dict] = ContextVar("current_user", default={})
