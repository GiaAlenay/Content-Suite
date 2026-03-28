import io
import logging
from typing import Dict, Any
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor, whitesmoke, slategray


class PDFGeneratorService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configuración de la identidad visual del documento PDF"""
        # Título Principal
        self.styles.add(
            ParagraphStyle(
                name="ManualTitle",
                fontSize=24,
                leading=28,
                alignment=TA_CENTER,
                spaceAfter=40,
                fontName="Helvetica-Bold",
                textColor=HexColor("#1A252F"),
            )
        )

        # Subtítulos de Secciones (del Schema)
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                fontSize=14,
                leading=18,
                alignment=TA_LEFT,
                spaceBefore=20,
                spaceAfter=12,
                fontName="Helvetica-Bold",
                textColor=HexColor("#2980B9"),
                borderPadding=5,
            )
        )

        # Texto de Cuerpo Profesional
        self.styles.add(
            ParagraphStyle(
                name="NormalBody",
                fontSize=10.5,
                leading=14,
                alignment=TA_LEFT,
                fontName="Helvetica",
                spaceAfter=8,
            )
        )

        # Estilo para etiquetas (Labels)
        self.styles.add(
            ParagraphStyle(
                name="LabelStyle",
                fontSize=10,
                fontName="Helvetica-Bold",
                textColor=slategray,
            )
        )

    def _format_markdown_to_platypus(self, text: str):
        """Convierte Markdown simple a etiquetas compatibles con ReportLab"""
        # Limpieza básica para evitar errores de renderizado
        clean_text = text.replace("**", "<b>").replace("__", "<b>")
        clean_text = clean_text.replace("</b></b>", "</b>")  # Fix por si acaso

        paragraphs = []
        for line in clean_text.split("\n"):
            line = line.strip()
            if not line:
                continue

            # Detectar encabezados en el contenido generado
            if line.startswith("###"):
                paragraphs.append(
                    Paragraph(
                        line.replace("###", "").strip(), self.styles["SectionHeader"]
                    )
                )
            elif line.startswith("##"):
                paragraphs.append(Spacer(1, 10))
                paragraphs.append(
                    Paragraph(
                        line.replace("##", "").strip(), self.styles["SectionHeader"]
                    )
                )
            else:
                paragraphs.append(Paragraph(line, self.styles["NormalBody"]))

        return paragraphs

    def create_brand_manual_pdf(
        self, brand_name: str, brand_code: str, parameters: Dict[str, Any], content: str
    ) -> bytes:
        """Genera el PDF en memoria y devuelve los bytes"""
        logging.info(f"Generando PDF para la marca: {brand_name}")

        buffer = io.BytesIO()
        # Configuración del documento con márgenes profesionales
        doc = SimpleDocTemplate(
            buffer,
            pagesize=LETTER,
            rightMargin=50,
            leftMargin=50,
            topMargin=60,
            bottomMargin=50,
        )

        story = []

        # --- PORTADA / TÍTULO ---
        story.append(Spacer(1, 40))
        story.append(
            Paragraph(f"Manual de Identidad de Marca", self.styles["ManualTitle"])
        )
        story.append(
            Paragraph(f"{brand_name.upper()} ({brand_code})", self.styles["NormalBody"])
        )
        story.append(Spacer(1, 30))
        story.append(Paragraph("<hr/>", self.styles["NormalBody"]))  # Línea divisoria
        story.append(Spacer(1, 20))

        # --- SECCIÓN 1: RESUMEN DE PARÁMETROS (Input del Schema) ---
        story.append(
            Paragraph("Resumen de Configuración", self.styles["SectionHeader"])
        )

        # Preparar datos para una tabla de resumen limpia
        table_data = [
            [
                Paragraph("Audiencia Objetivo:", self.styles["LabelStyle"]),
                Paragraph(
                    parameters.get("target_audience", "N/A"), self.styles["NormalBody"]
                ),
            ],
            [
                Paragraph("Valores Nucleares:", self.styles["LabelStyle"]),
                Paragraph(
                    ", ".join(parameters.get("core_values", [])),
                    self.styles["NormalBody"],
                ),
            ],
            [
                Paragraph("Tono de Voz:", self.styles["LabelStyle"]),
                Paragraph(
                    parameters.get("tone_preference", "N/A"), self.styles["NormalBody"]
                ),
            ],
            [
                Paragraph("Estilo Visual:", self.styles["LabelStyle"]),
                Paragraph(
                    parameters.get("visual_style", "N/A"), self.styles["NormalBody"]
                ),
            ],
            [
                Paragraph("Colores Principales:", self.styles["LabelStyle"]),
                Paragraph(
                    ", ".join(parameters.get("brand_colors", [])),
                    self.styles["NormalBody"],
                ),
            ],
        ]

        summary_table = Table(table_data, colWidths=[120, 380])
        summary_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )
        story.append(summary_table)

        # --- SALTO DE PÁGINA ---
        story.append(PageBreak())

        # --- SECCIÓN 2: CONTENIDO GENERADO (Estrategia Completa) ---
        story.append(
            Paragraph("Estrategia y Definición de Marca", self.styles["SectionHeader"])
        )
        story.append(Spacer(1, 10))

        # Procesar el contenido de la IA (Markdown a Platypus)
        body_elements = self._format_markdown_to_platypus(content)
        story.extend(body_elements)

        # --- PIE DE PÁGINA (Nota de auditoría) ---
        story.append(Spacer(1, 40))
        story.append(Paragraph("<hr/>", self.styles["NormalBody"]))
        footer_text = "Generado automáticamente por Content-Suite - Inteligencia Artificial y Gobernanza de Marca."
        story.append(
            Paragraph(
                footer_text,
                ParagraphStyle(
                    name="Footer", fontSize=8, textColor=slategray, alignment=TA_CENTER
                ),
            )
        )

        # Construir
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes
