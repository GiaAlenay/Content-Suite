import { Stack, Button, CircularProgress } from "@mui/material";

interface NavigationButtonsProps {
  activeStep: number;
  setActiveStep: (step: (prev: number) => number) => void;
  isLastStep: boolean;
  isAuditing: boolean;
  isRefining: boolean;
  isConfirming: boolean;
}

export const NavigationButtons = ({
  activeStep,
  setActiveStep,
  isLastStep,
  isAuditing,
  isRefining,
  isConfirming,
}: NavigationButtonsProps) => {
  const handleNext = () => setActiveStep((prev) => prev + 1);
  const handleBack = () => setActiveStep((prev) => prev - 1);

  return (
    <Stack
      direction="row"
      sx={{
        mt: "auto",
        pt: 2,
        borderTop: "1px solid #eee",
        justifyContent: "space-between",
        alignItems: "center",
        gap: 1.5,
      }}
    >
      {activeStep > 0 && (
        <Button
          variant="outlined"
          onClick={handleBack}
          sx={{ textTransform: "none", minWidth: "100px" }}
        >
          Atrás
        </Button>
      )}

      {isLastStep ? (
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={isAuditing || isRefining || isConfirming}
          sx={{ minWidth: "100px !important" }}
        >
          {isAuditing ? (
            <div className="loadingBtn">
              <CircularProgress size={20} style={{ color: "#FFFFFF" }} />
            </div>
          ) : (
            <>Generar</>
          )}
        </Button>
      ) : (
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={isAuditing}
          sx={{
            minWidth: `${activeStep > 0 ? "100px !important" : "100% !important"}`,
          }}
        >
          Continuar
        </Button>
      )}
    </Stack>
  );
};
