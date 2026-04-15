from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List


class BrandConflict(BaseModel):
    point: str = Field(
        description="El elemento específico en conflicto (ej: Tono, Colores, Audiencia)"
    )
    reason: str = Field(description="Por qué contradice la esencia de la marca")
    suggestion: str = Field(description="Cómo alinearlo para mantener la coherencia")


class AuditReport(BaseModel):
    is_coherent: bool = Field(description="¿Debe permitirse la generación del manual?")
    severity: str = Field(description="LOW, MEDIUM, HIGH")
    human_message: str = Field(
        description="Mensaje redactado por el agente para el usuario final explicando el resultado, "
        "incluyendo sugerencias si es necesario."
    )

    conflicts: List[BrandConflict] = Field(default_factory=list)


class ParamsAuditAgent:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(AuditReport)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres el 'Guardian of Brand Integrity' (GBI). Tu función no es solo validar datos, "
                        "sino asegurar que la esencia estratégica de la marca no se diluya ni se contradiga.\n\n"
                        "PROTOCOLO DE AUDITORÍA CRÍTICA:\n"
                        "1. COHERENCIA DE VALORES: Evalúa si los 'Core Values' solicitados chocan con la 'Descripción Base'.\n"
                        "2. ALINEACIÓN SOCIOGRÁFICA: ¿Es el tono solicitado el adecuado para la Audiencia descrita?\n"
                        "3. INTEGRIDAD VISUAL: Verifica que el estilo visual y colores no transmitan sensaciones opuestas al ADN de marca.\n"
                        "4. FILTRO DE PROHIBICIONES: Asegura que los requerimientos no ignoren las restricciones impuestas.\n\n"
                        "ESCALA DE SEVERIDAD Y ACCIÓN:\n"
                        "- LOW: Desviaciones mínimas. El mensaje humano debe ser motivador y sugerir ajustes sutiles. is_coherent=True.\n"
                        "- MEDIUM: Inconsistencias notables que requieren atención. El mensaje debe ser una advertencia clara. is_coherent=True.\n"
                        "- HIGH: Violaciones críticas al ADN de marca. Bloqueo total. El mensaje debe ser firme, educativo y explicar por qué no se puede proceder sin cambios radicales. is_coherent=False.\n\n"
                        "DIRECTRICES PARA EL 'HUMAN_MESSAGE':\n"
                        "- Actúa como un mentor, no como un error de sistema.\n"
                        "- En caso de HIGH severity, inicia explicando el valor de la marca que estás protegiendo.\n"
                        "- Usa un lenguaje profesional, empático y constructivo.\n"
                        "- El mensaje debe ser autoconclusivo: el usuario debe entender exactamente qué hacer a continuación."
                    ),
                ),
                (
                    "user",
                    (
                        "AUDITORÍA REQUERIDA PARA EL SIGUIENTE ESCENARIO:\n\n"
                        "--- ADN DE MARCA (CONTEXTO) ---\n"
                        "{brand_desc}\n\n"
                        "--- PARÁMETROS DE NUEVA GENERACIÓN ---\n"
                        "• Audiencia Objetivo: {target}\n"
                        "• Valores Propuestos: {values}\n"
                        "• Tono Seleccionado: {tone}\n"
                        "• Temas Prohibidos: {forbidden}\n"
                        "• Configuración Visual: {visual}\n\n"
                        "POR FAVOR, GENERA EL REPORTE ESTRUCTURADO."
                    ),
                ),
            ]
        )

    async def execute(self, brand_desc: str, params: dict) -> AuditReport:
        inputs = {
            "brand_desc": brand_desc,
            "target": params.get("target_audience", "No definido"),
            "values": ", ".join(params.get("core_values", [])),
            "tone": params.get("tone_preference", "No definido"),
            "forbidden": ", ".join(params.get("forbidden_topics", [])),
            "visual": (
                f"Estilo {params.get('visual_style', 'No definido')} "
                f"con colores {params.get('brand_colors', 'No definido')}. "
                f"Guías de Logo: {params.get('logo_guidelines', 'No definido')}"
            ),
        }

        chain = self.prompt | self.llm
        report: AuditReport = await chain.ainvoke(inputs)

        if report.severity == "HIGH":
            report.is_coherent = False
        elif report.severity == "LOW" or report.severity == "MEDIUM":
            report.is_coherent = True

        return report
