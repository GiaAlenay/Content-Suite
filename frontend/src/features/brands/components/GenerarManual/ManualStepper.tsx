import { Stepper, Step, StepLabel, Box, styled } from "@mui/material";
import StepConnector, {
  stepConnectorClasses,
} from "@mui/material/StepConnector";

const QontoConnector = styled(StepConnector)(({ theme }) => ({
  [`&.${stepConnectorClasses.alternativeLabel}`]: {
    top: 10,
    left: "calc(-50% + 16px)",
    right: "calc(50% + 16px)",
  },
  [`&.${stepConnectorClasses.active}`]: {
    [`& .${stepConnectorClasses.line}`]: {
      borderColor: theme.palette.primary.main,
    },
  },
  [`&.${stepConnectorClasses.completed}`]: {
    [`& .${stepConnectorClasses.line}`]: {
      borderColor: theme.palette.primary.main,
    },
  },
  [`& .${stepConnectorClasses.line}`]: {
    borderColor:
      theme.palette.mode === "dark" ? theme.palette.grey[800] : "#eaeaf0",
    borderTopWidth: 3,
    borderRadius: 1,
    transition: "all 0.5s ease-in-out",
  },
}));

// 2. Icono personalizado (Círculo vacío)
const QontoStepIconRoot = styled("div")(({ theme, ownerState }) => ({
  color: theme.palette.mode === "dark" ? theme.palette.grey[700] : "#eaeaf0",
  display: "flex",
  height: 22,
  alignItems: "center",
  ...(ownerState.active && {
    color: theme.palette.primary.main,
  }),
  "& .QontoStepIcon-circle": {
    width: 12,
    height: 12,
    borderRadius: "50%",
    backgroundColor: "currentColor",
    transition: "transform 0.3s ease-in-out",
    ...(ownerState.active && {
      transform: "scale(1.3)", // Efecto de pulso al estar activo
    }),
  },
  ...(ownerState.completed && {
    color: theme.palette.primary.main,
  }),
}));

function QontoStepIcon(props) {
  const { active, completed, className } = props;
  return (
    <QontoStepIconRoot ownerState={{ active, completed }} className={className}>
      <div className="QontoStepIcon-circle" />
    </QontoStepIconRoot>
  );
}

const steps = ["Estrategia", "Identidad", "Finalizar"];

export const ManualStepper = ({ activeStep }: { activeStep: number }) => {
  return (
    <Box sx={{ width: "100%" }}>
      <Stepper
        activeStep={activeStep}
        alternativeLabel
        connector={<QontoConnector />} // Usamos el conector animado
      >
        {steps.map((label, i) => (
          <Step key={label}>
            <StepLabel
              StepIconComponent={QontoStepIcon} // Usamos el círculo vacío
            >
              <Box sx={{ textAlign: "center", mt: 1 }}>
                {/* Texto superior: STEP X */}
                <Box
                  sx={{
                    fontSize: "0.7rem",
                    fontWeight: 700,
                    textTransform: "uppercase",
                    color: "text.secondary",
                    letterSpacing: "0.05rem",
                    lineHeight: 1,
                  }}
                >
                  Paso {i + 1}
                </Box>

                <Box
                  sx={{
                    fontSize: "1rem",
                    fontWeight: 700,
                    color: "#0F172A",
                    mt: 0.8,
                    lineHeight: 1.1,
                    fontFamily: "Inter",
                  }}
                >
                  {label}
                </Box>
              </Box>
            </StepLabel>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
};
