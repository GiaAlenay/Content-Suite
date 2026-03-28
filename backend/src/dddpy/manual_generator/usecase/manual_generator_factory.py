from dddpy.manual_generator.usecase.manual_architect_agent import (
    BrandArchitectAgent,
)
from dddpy.manual_generator.usecase.manual_generator_usecase import (
    ManualGeneratorUseCase,
)
from dddpy.brand.usecase.brand_factory import brand_query_usecase_factory
from dddpy.manual_record.usecase.manual_record_factory import (
    manual_record_cmd_usecase_factory,
    manual_record_query_usecase_factory,
)

from dddpy.brand_manual_vector.usecase.brand_manual_vector_factory import (
    brand_manual_vector_cmd_usecase_factory,
)

from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.manual_generator.usecase.manual_governance_audit_agent import (
    ManualGovernanceAuditor,
)


def brand_architect_agent_factory():
    return BrandArchitectAgent()


def manual_governance_audit_agent_agent_factory():
    return ManualGovernanceAuditor()


def manual_generator_usecase_factory():
    return ManualGeneratorUseCase(
        brand_query=brand_query_usecase_factory(),
        manual_record_cmd=manual_record_cmd_usecase_factory(),
        manual_record_query=manual_record_query_usecase_factory(),
        vector_cmd=brand_manual_vector_cmd_usecase_factory(),
        vectorize_service=VectorizationService(),
        brand_architect=brand_architect_agent_factory(),
        manual_prompt_auditor=manual_governance_audit_agent_agent_factory(),
    )
