from dddpy.manual_generator.usecase.manual_architect_agent import (
    BrandArchitectAgent,
)
from dddpy.manual_generator.usecase.manual_generator_usecase import (
    ManualGeneratorUseCase,
)
from dddpy.brand.usecase.brand_factory import brand_query_usecase_factory

from dddpy.manual_version.usecase.manual_version_factory import (
    manual_version_cmd_usecase_factory,
    manual_version_query_usecase_factory,
)

from dddpy.manual_section.usecase.manual_section_factory import (
    manual_section_cmd_usecase_factory,
    manual_section_query_usecase_factory,
)

from dddpy.brand_manual_vector.usecase.brand_manual_vector_factory import (
    brand_manual_vector_cmd_usecase_factory,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_factory import (
    brand_manual_vector_query_usecase_factory,
)
from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.manual_generator.usecase.manual_governance_audit_agent import (
    ManualGovernanceAuditor,
)
from dddpy.manual_generator.usecase.manual_generator_pdf import PDFGeneratorService
from dddpy.shared.upload.upload import StorageService
from dddpy.shared.supabase.checkpoint_manager import get_db_checkpointer as checkpointer
from dddpy.manual_generator.infraestructure.ai.model_factory import model_factory
from dddpy.manual_generator.infraestructure.ai.graph import create_manual_graph
from dddpy.manual_generator.infraestructure.ai.agents.ParamsAuditAgent import (
    ParamsAuditAgent,
)
from dddpy.manual_generator.infraestructure.ai.agents.ArchitectAgent import (
    ArchitectAgent,
)
from dddpy.manual_generator.infraestructure.ai.agents.IntentOrchestratorAgent import (
    IntentOrchestratorAgent,
)

from dddpy.manual_generator.infraestructure.ai.agents.PromptAuditAgent import (
    PromptAuditAgent,
)

from dddpy.manual_generator.infraestructure.ai.agents.ContextDiscoveryAgent import (
    ContextDiscoveryAgent,
)

from dddpy.manual_generator.infraestructure.ai.agents.PromptUpgraderAgent import (
    PromptUpgraderAgent,
)
from dddpy.manual_generator.infraestructure.ai.agents.QAAgent import QAAgent
from dddpy.manual_generator.infraestructure.ai.agents.EditorAgent import EditorAgent

from dddpy.chat_session.usecase.chat_session_factory import (
    chat_session_cmd_usecase_factory,
    chat_session_query_usecase_factory,
)

from dddpy.chat_history.usecase.chat_history_factory import (
    chat_history_cmd_usecase_factory,
    chat_history_query_usecase_factory,
)
from dddpy.manual_generator.usecase.manual_generator_pdf import PDFGeneratorService
from dddpy.shared.upload.upload import StorageService


def brand_architect_agent_factory():
    return BrandArchitectAgent()


def manual_governance_audit_agent_agent_factory():
    return ManualGovernanceAuditor(
        vector_repo=brand_manual_vector_query_usecase_factory(),
        vectorize_service=VectorizationService(),
    )


def manual_pdf_generator_factory():
    return PDFGeneratorService()


def storage_service_factory():
    return StorageService()


def manual_graph_factory(checkpointer):

    llm = model_factory()

    architect_agent = ArchitectAgent(llm)
    context_discovery_agent = ContextDiscoveryAgent(llm)
    editor_agent = EditorAgent(llm)
    intent_specify_agent = IntentOrchestratorAgent(llm)
    params_auditor_agent = ParamsAuditAgent(llm)
    prompt_auditor_agent = PromptAuditAgent(llm)
    prompt_upgrade_agent = PromptUpgraderAgent(llm)
    qa_agent = QAAgent(llm)

    chat_session_cmd = chat_session_cmd_usecase_factory()
    chat_session_query = chat_session_query_usecase_factory()
    chat_history_cmd = chat_history_cmd_usecase_factory()
    chat_history_query = chat_history_query_usecase_factory()
    manual_version_cmd = manual_version_cmd_usecase_factory()
    manual_version_query = manual_version_query_usecase_factory()
    manual_section_cmd = manual_section_cmd_usecase_factory()
    brand_manual_vector_cmd = brand_manual_vector_cmd_usecase_factory()
    vectorize_service = VectorizationService()
    pdf_generator_service = PDFGeneratorService()
    storage_service = StorageService()

    graph = create_manual_graph(
        checkpointer=checkpointer,
        params_auditor_agent=params_auditor_agent,
        editor_agent=editor_agent,
        architect_agent=architect_agent,
        prompt_upgrade_agent=prompt_upgrade_agent,
        intent_specify_agent=intent_specify_agent,
        prompt_auditor_agent=prompt_auditor_agent,
        context_discovery_agent=context_discovery_agent,
        qa_agent=qa_agent,
        chat_session_cmd=chat_session_cmd,
        chat_session_query=chat_session_query,
        chat_history_cmd=chat_history_cmd,
        chat_history_query=chat_history_query,
        vectorize_service=vectorize_service,
        pdf_generator_service=pdf_generator_service,
        storage_service=storage_service,
        manual_version_cmd=manual_version_cmd,
        manual_version_query=manual_version_query,
        manual_section_cmd=manual_section_cmd,
        brand_manual_vector_cmd=brand_manual_vector_cmd,
    )

    return graph


def manual_generator_usecase_factory():
    return ManualGeneratorUseCase(
        graph_builder=manual_graph_factory(checkpointer),
        brand_query=brand_query_usecase_factory(),
        manual_version_cmd=manual_version_cmd_usecase_factory(),
        manual_version_query=manual_version_query_usecase_factory(),
        vector_cmd=brand_manual_vector_cmd_usecase_factory(),
        vectorize_service=VectorizationService(),
        brand_architect=brand_architect_agent_factory(),
        manual_prompt_auditor=manual_governance_audit_agent_agent_factory(),
        pdf_generator=manual_pdf_generator_factory(),
        storage=storage_service_factory(),
    )
