from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dddpy.shared.langfuse_tracing.observability import audit_trace
from dddpy.content_log.usecase.governance_audit_agent import GovernanceAuditAgent
from dddpy.manual_generator.usecase.manual_generator_schema import AuditManualSchema


class ManualGovernanceAuditor(GovernanceAuditAgent):
    def __init__(self, vector_repo, vectorize_service):
        super().__init__(vector_repo, vectorize_service)
        self.manual_parser = JsonOutputParser(pydantic_object=AuditManualSchema)

    # # @audit_trace(name="Manual Governance - Parameter Consistency")
    async def verify_manual_params(
        self, brand_description: str, raw_params: dict
    ) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Senior Brand Strategist. Tu misión es auditar los PARÁMETROS "
                        "de entrada para la creación de un Manual de Identidad.\n"
                        "Debes detectar si lo que el usuario pide contradice la NATURALEZA "
                        "de la marca definida en su descripción.\n\n"
                        "{format_instructions}"
                        "Eres un Senior Brand Strategist. Tu misión es auditar los PARÁMETROS "
                        "de entrada para la creación o refinamiento de un Manual de Identidad.\n\n"
                        "### REGLAS DE PRIORIDAD Y AUTORIDAD:\n"
                        "1. LA DESCRIPCIÓN DE MARCA es la 'Constitución'. Nada puede ir en contra de su esencia base.\n"
                        "2. Las INSTRUCCIONES DE REFINAMIENTO (si existen) tienen prioridad sobre los parámetros originales del formulario, "
                        "siempre y cuando no rompan la Regla 1.\n"
                        "3. Tu juicio debe ser OBJETIVO: Diferencia entre una 'evolución de la marca' (permitido) y una 'ruptura de identidad' (bloqueante).\n"
                        "4. Debes detectar si lo que el usuario pide contradice la NATURALEZA \n"
                        "de la marca definida en su descripción.\n"
                        "{format_instructions}"
                    ),
                ),
                (
                    "user",
                    (
                        "### CONTEXTO PARA AUDITORÍA:\n"
                        "DESCRIPCIÓN DE LA MARCA:\n{brand_desc}\n\n"
                        "PARÁMETROS DEL FORMULARIO:\n{params}\n\n"
                        "CRITERIOS DE AUDITORÍA:\n"
                        "1. ¿El tono pedido es coherente con el rubro de la marca?\n"
                        "2. ¿Los valores nucleares chocan con la descripción?\n"
                        "3. ¿Las notas adicionales piden algo que rompa la identidad base?\n"
                        "4. ¿La nueva instrucción es coherente con la descripción base?\n"
                        "5. ¿Hay contradicciones lógicas que el usuario deba corregir?\n"
                        "6. Determina SEVERITY: 'HIGH' si rompe la identidad base, 'LOW' si es solo una observación.\n"
                        "7. ¿La identidad visual (colores y estilo) es coherente con el sector y la descripción de la marca?\n"
                        "8. ¿Las reglas del logo son lógicas para el tipo de empresa?"
                    ),
                ),
            ]
        ).partial(format_instructions=self.manual_parser.get_format_instructions())

        # En este flujo usamos el modelo de texto (Llama 3.3 70B) por su alta capacidad de razonamiento
        chain = prompt | self.llm_text | self.manual_parser

        return chain.invoke(
            {"brand_desc": brand_description, "params": str(raw_params)}
        )
