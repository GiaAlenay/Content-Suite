import { useEffect, useState } from "react";
import type {
  AuditManualResponse,
  ManualRecord,
} from "../interfaces/ManualGeneratorData";
import { useParams } from "react-router-dom";
import { FormProvider, useForm } from "react-hook-form";
import {
  GenerateManualSchema,
  type GenerateManualInputs,
} from "../schemas/generarManual";
import { zodResolver } from "@hookform/resolvers/zod";
import { useManualGenerator } from "../hooks/useManualGenerator";
import { Box } from "@mui/material";
import { ManualStepper } from "../components/GenerarManual/ManualStepper";
import { NavigationButtons } from "../components/GenerarManual/NavigationButtons";
import { EmptyStateIA } from "../components/GenerarManual/EmptyStateIA";
import { AuditReportPanel } from "../components/GenerarManual/AuditReportPanel";
import { StrategicSection } from "../components/GenerarManual/steps/StrategicSection";
import { VisualSection } from "../components/GenerarManual/steps/VisualSection";
import { AdditionalSection } from "../components/GenerarManual/steps/AdditionalSection";
import { ManualWorkspace } from "../components/GenerarManual/ManualWorkspace";

export const mockAuditHighSeverity: AuditManualResponse = {
  is_coherent: false,
  severity: "HIGH",
  feedback: [
    "Los colores elegidos (#FF0000, #000000) contradicen el valor de 'Sostenibilidad y Naturaleza'.",
    "El tono 'Agresivo y Competitivo' entra en conflicto con la misión de 'Comercio Justo'.",
    "La audiencia 'Niños' no coincide con el estilo visual 'Ejecutivo Minimalista'.",
  ],
  suggestions:
    "Cambia la paleta a tonos tierra (#4A5D23) y ajusta el tono a uno más 'Educativo y Empático' para alinearte con el origen orgánico de Andina Foods.",
};

// 2. Escenario: Auditoría con sugerencias (LOW Severity)
export const mockAuditLowSeverity: AuditManualResponse = {
  is_coherent: true, // Es coherente, pero con observaciones
  severity: "LOW",
  feedback: [
    "La audiencia es un poco amplia; considera segmentar más el mercado europeo.",
    "El valor 'Innovación' podría detallarse más en las notas adicionales.",
  ],
  suggestions:
    "El borrador se generará, pero se recomienda ser más específico en los 'Temas Prohibidos' para evitar menciones a la competencia indirecta.",
};

export const mockManualRecord: ManualRecord = {
  id: "man_abc123",
  brand_id: "andina_foods_id",
  version: 1,
  full_manual: `
# Manual de Identidad de Marca: Andina Foods

## 1. Esencia de Marca
Andina Foods es una exportadora de superalimentos que conecta la **herencia ancestral de los Andes** con el mercado global. 

## 2. Voz y Tono
Nuestro tono es **Experto y Orgulloso**. No solo vendemos granos, compartimos una cultura.
* **Hacer:** Usar datos técnicos sobre nutrición.
* **No hacer:** Usar lenguaje excesivamente informal o juvenil.

## 3. Identidad Visual
### Paleta de Colores
* **Verde Olivo (#4A5D23):** Representa nuestros campos y la sostenibilidad.
* **Ocre Tierra (#D4A373):** El color de la quinua y la tierra fértil.

### Estilo Fotográfico
Siempre usar luz natural. Las fotos deben mostrar la textura real de la **maca** y la **kiwicha**.

## 4. Lineamientos de Comunicación
Queda estrictamente prohibido comparar nuestros productos con alimentos procesados de bajo costo.
  `,
  raw_parameters: {
    target_audience: "Consumidores B2B en Europa y EE.UU.",
    core_values: ["Ancestralidad", "Sostenibilidad", "Calidad Premium"],
    tone_preference: "Profesional, experto y orgulloso",
    forbidden_topics: ["Comida Ultraprocesada", "Químicos"],
    brand_colors: ["#4A5D23", "#D4A373", "#F1EAD7"],
    visual_style: "Rústico-Moderno con texturas orgánicas",
    additional_notes: "Incluir historia de los Andes como respaldo.",
  },
  is_current_version: false,
  agent_feedback: mockAuditLowSeverity,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
};

export const ManualGeneratorPage = () => {
  const { idBrand } = useParams();
  const [activeStep, setActiveStep] = useState(0);
  const [draftManual, setDraftManual] = useState<ManualRecord | null>(null);
  const [auditResult, setAuditResult] = useState<AuditManualResponse | null>(
    null,
  );

  const methods = useForm<GenerateManualInputs>({
    resolver: zodResolver(GenerateManualSchema),
    mode: "onBlur",
    defaultValues: {
      core_values: [],
      brand_colors: [],
      forbidden_topics: [],
    },
  });

  const {
    auditManual,
    isAuditing,
    refineManual,
    isRefining,
    confirmManual,
    isConfirming,
  } = useManualGenerator();

  // --- FLUJO 1: AUDITAR / GENERAR INICIAL ---
  const handleProcessIA = async (data: GenerateManualInputs) => {
    if (!idBrand) return;

    // Limpiamos estados previos antes de nueva auditoría
    setAuditResult(null);
    setDraftManual(null);

    const result = await auditManual({ idBrand, raw_parameters: data });

    // El backend devuelve AuditManualResponse si hay errores de coherencia
    // O ManualRecord si todo está bien y ya generó el borrador
    if ("is_coherent" in result && !result.is_coherent) {
      setAuditResult(result);
    } else {
      // Si es coherente, el resultado es el ManualRecord (draft)
      setDraftManual(result as ManualRecord);
    }
  };

  // --- FLUJO 2: REFINAR (Iterar sobre el borrador) ---
  const handleRefine = async (prompt: string) => {
    if (!draftManual?.id) return;

    const result = await refineManual({
      manualId: draftManual.id,
      refinement_prompt: prompt,
    });

    // Actualizamos el borrador con la nueva versión generada por la IA
    if (!("is_coherent" in result)) {
      setDraftManual(result as ManualRecord);
      setAuditResult(null); // Limpiamos reportes de auditoría si existían
    }
  };

  // --- FLUJO 3: CONFIRMAR (Guardado final) ---
  const handleConfirm = async () => {
    if (!draftManual?.id) return;

    try {
      await confirmManual(draftManual.id);
      // Aquí podrías redirigir al usuario o mostrar un mensaje de éxito
      console.log("Manual confirmado con éxito");
      // Ejemplo: navigate(`/brands/${idBrand}`);
    } catch (error) {
      console.error("Error al confirmar:", error);
    }
  };
  return (
    <Box
      sx={{
        display: "flex",
        padding: "24px 32px",
        borderRadius: "8px",
        background: "#fff",
        border: "1px solid rgba(0, 0, 0, 0.12)",
        boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
        height: "94vh",
        overflow: "hidden",
      }}
    >
      <FormProvider {...methods}>
        <div
          className="column-base"
          style={{
            width: "45%",
            padding: "36px",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "60px",
            height: "100%",
            boxSizing: "border-box",
          }}
        >
          <ManualStepper activeStep={activeStep} />

          <form
            onSubmit={methods.handleSubmit(handleProcessIA)}
            style={{
              background: "white",
              flex: 1,
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div style={{ flex: 1 }}>
              {activeStep === 0 && <StrategicSection />}
              {activeStep === 1 && <VisualSection />}
              {activeStep === 2 && <AdditionalSection />}
            </div>

            <NavigationButtons
              activeStep={activeStep}
              setActiveStep={setActiveStep}
              isLastStep={activeStep === 2}
              isAuditing={isAuditing}
              isRefining={isRefining}
              isConfirming={isConfirming}
            />
          </form>
        </div>

        <Box
          sx={{ width: "55%", bgcolor: "#fcf6f6ff", p: 4, overflowY: "auto" }}
        >
          {!draftManual && !auditResult && <EmptyStateIA />}

          {auditResult && <AuditReportPanel report={auditResult} />}

          {draftManual && (
            <ManualWorkspace
              manual={draftManual}
              onRefine={handleRefine}
              handleConfirm={handleConfirm}
              isRefining={isRefining}
              isConfirming={isConfirming}
            />
          )}
        </Box>
      </FormProvider>
    </Box>
  );
};
