from dddpy.manual_generator.infraestructure.ai.agents.ParamsAuditAgent import (
    ParamsAuditAgent,
)
from dddpy.manual_generator.infraestructure.ai.agents.ArchitectAgent import (
    ArchitectAgent,
)
from dddpy.manual_generator.infraestructure.ai.state import ManualState


async def node_params_audit(state: ManualState, params_auditor_agent: ParamsAuditAgent):
    report = await params_auditor_agent.execute(
        state["brand_description"], state["raw_params"]
    )

    return {
        "audit_report": report.dict(),
        "next_step": (
            "generate" if report.is_coherent and report.severity != "HIGH" else "stop"
        ),
        "messages": [("assistant", report.human_message)],
    }


async def node_architect(state: ManualState, architect_agent: ArchitectAgent):
    """Paso 2: Redactar contenido compdel manual"""
    content = await architect_agent.execute(
        brand_name=state["brand_name"],
        brand_description=state["brand_description"],
        raw_params=state["raw_params"],
    )
    return {"full_content": content}
