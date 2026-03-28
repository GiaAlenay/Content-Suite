from dddpy.content_log.infrastructure.content_log_cmd_repository import (
    ContentLogCmdRepositoryImpl,
)
from dddpy.content_log.infrastructure.content_log_query_repository import (
    ContentLogQueryRepositoryImpl,
)
from dddpy.content_log.usecase.content_log_cmd_usecase import ContentLogCmdUseCase
from dddpy.content_log.usecase.content_log_query_usecase import ContentLogQueryUseCase
from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.content_log.usecase.creative_agent import (
    CreativeEngineAgent,
)
from dddpy.brand.usecase.brand_factory import brand_query_usecase_factory
from dddpy.brand_manual_vector.usecase.brand_manual_vector_factory import (
    brand_manual_vector_query_usecase_factory,
)
from dddpy.content_log.usecase.content_log_usecase import ContentLogUseCase
from dddpy.content_log.usecase.governance_audit_agent import (
    GovernanceAuditAgent,
)


# --- Factories de Repositorios (Nivel Bajo) ---
def content_log_cmd_repository_factory():
    return ContentLogCmdRepositoryImpl()


def content_log_query_repository_factory():
    return ContentLogQueryRepositoryImpl()


# --- Factories de UseCases Simples ---
def content_log_cmd_usecase_factory():
    return ContentLogCmdUseCase(content_log_cmd_repository_factory())


def content_log_query_usecase_factory():
    return ContentLogQueryUseCase(content_log_query_repository_factory())


# --- Factory del Agente Creativo ---
def creative_engine_factory():
    # Inyectamos las herramientas que el agente necesita
    return CreativeEngineAgent(
        vector_repo=brand_manual_vector_query_usecase_factory(),
        vectorize_service=VectorizationService(),
    )


def governance_agent_factory():
    # Inyectamos las herramientas que el auditor necesita
    return GovernanceAuditAgent(
        vector_repo=brand_manual_vector_query_usecase_factory(),
        vectorize_service=VectorizationService(),
    )


# --- Factory del UseCase Principal (Nivel Alto) ---
def content_log_usecase_factory():
    return ContentLogUseCase(
        content_log_cmd=content_log_cmd_usecase_factory(),
        content_log_query=content_log_query_usecase_factory(),
        brand_query=brand_query_usecase_factory(),
        content_generator=creative_engine_factory(),
        auditor=governance_agent_factory(),
    )
