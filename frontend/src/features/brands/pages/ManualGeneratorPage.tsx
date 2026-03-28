import { useState } from "react";
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
import { useManualGenerator } from "../hooks/useBrands copy";
import { Box } from "@mui/material";
import { ManualStepper } from "../components/GenerarManual/ManualStepper";
import { NavigationButtons } from "../components/GenerarManual/NavigationButtons";
import { EmptyStateIA } from "../components/GenerarManual/EmptyStateIA";
import { AuditReportPanel } from "../components/GenerarManual/AuditReportPanel";
import { StrategicSection } from "../components/GenerarManual/steps/StrategicSection";
import { VisualSection } from "../components/GenerarManual/steps/VisualSection";
import { AdditionalSection } from "../components/GenerarManual/steps/AdditionalSection";
import { ManualWorkspace } from "../components/GenerarManual/ManualWorkspace";

export const ManualGeneratorPage = () => {
  const { idBrand } = useParams();
  const [activeStep, setActiveStep] = useState(0);
  const [draftManual, setDraftManual] = useState<ManualRecord | null>(null);
  const [auditResult, setAuditResult] = useState<AuditManualResponse | null>(
    null,
  );

  // 1. Inicializar Formulario
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

  const handleProcessIA = async (data: GenerateManualInputs) => {
    if (!idBrand) return; //agregar logica
    const result = await auditManual({ idBrand, raw_parameters: data });

    if ("is_coherent" in result) {
      setAuditResult(result);
    } else {
      setDraftManual(result);
    }
  };

  const handleRefine = async () => {};
  const handleConfirm = async () => {};

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
              onConfirm={handleConfirm}
              isRefining={isRefining}
              isConfirming={isConfirming}
            />
          )}
        </Box>
      </FormProvider>
    </Box>
  );
};
