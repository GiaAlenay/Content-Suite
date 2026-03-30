import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Stack,
  TextField,
  MenuItem,
  Box,
  Alert,
  CircularProgress,
  IconButton,
  Typography,
  Grid,
  Snackbar,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import AutoFixHighIcon from "@mui/icons-material/AutoFixHigh";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  GenerateContentSchema,
  type GenerateContentInputs,
} from "../../schemas/agregarContentLog";
import type {
  AuditPromptResponse,
  ContentLogInterface,
} from "../../interfaces/ContentLogData";
import { IconBellRinging, IconCopy } from "@tabler/icons-react";
import type { BrandInterface } from "../../../brands/interfaces/BrandData";
import {
  auditarRequestQuestion,
  auditarRequestTitle,
  CONTENT_TYPE_OPTIONS,
} from "../../constants";
import { ConfirmActionModal } from "../../../../common/components/ConfirmActionModal/ConfirmActionModal";

interface Props {
  open: boolean;
  onClose: () => void;
  brands: BrandInterface[];
  isLoading: boolean;
  onSave: (
    data: GenerateContentInputs,
    action: () => void,
  ) => Promise<AuditPromptResponse | ContentLogInterface | undefined>;
  handleConfirm: (contentLogId?: string | null) => void;
}

export const AddContentLogModal: React.FC<Props> = ({
  open,
  onClose,
  brands,
  isLoading,
  handleConfirm,
  onSave,
}) => {
  const [isConfirmCambiarStatusOpen, setIsConfirmCambiarStatusOpen] =
    useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [generatedLog, setGeneratedLog] = useState<ContentLogInterface | null>(
    null,
  );
  const [audit, setAudit] = useState<AuditPromptResponse | null>(null);
  const { control, handleSubmit, setValue, watch, reset } =
    useForm<GenerateContentInputs>({
      resolver: zodResolver(GenerateContentSchema),
      defaultValues: { brand_id: "", content_type: "", user_prompt: "" },
    });

  const handleCloseConfirmCambiarStatus = () => {
    setIsConfirmCambiarStatusOpen(false);
  };

  const currentPrompt = watch("user_prompt");

  const handleGenerate = async (data: GenerateContentInputs) => {
    const response = await onSave(
      { ...data, parent_log_id: generatedLog?.id || null },
      () => {},
    );

    if (!response) return;

    if ("is_allowed" in response) {
      if (response.is_allowed === false || response.is_type_match === false) {
        setAudit(response as AuditPromptResponse);
      } else {
        setAudit(null);
      }
    } else {
      setGeneratedLog(response as ContentLogInterface);
      setAudit(null);
    }
  };

  const handleCopy = () => {
    const content =
      generatedLog?.content_data?.text ||
      generatedLog?.content_data?.generated_content;
    if (content) {
      navigator.clipboard.writeText(content);
      setSnackbarOpen(true);
    }
  };

  const handleApplyImprovement = () => {
    if (audit?.improved_prompt) {
      setValue("user_prompt", audit.improved_prompt);
      setAudit(null);
    }
  };

  const handleOpenConfirmCambiarStatus = () => {
    setIsConfirmCambiarStatusOpen(true);
  };

  const handleClose = () => {
    reset();
    setGeneratedLog(null);
    setAudit(null);
    onClose();
  };

  return (
    <>
      <Dialog open={open} onClose={handleClose} fullWidth maxWidth="xs">
        <DialogTitle
          sx={{
            gap: 1.5,
            fontWeight: "bold",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography variant="h6" fontWeight="bold" component="span">
            Generar Contenido
          </Typography>
          <Stack direction="row" spacing={1}>
            <IconButton onClick={handleClose}>
              <CloseIcon />
            </IconButton>
          </Stack>
        </DialogTitle>

        <DialogContent dividers>
          <Box component="form" sx={{ mt: 2.5 }}>
            <Grid sx={{ mt: 2.5 }}>
              <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
                Marca *
              </Typography>
              <Controller
                name="brand_id"
                control={control}
                render={({ field, fieldState }) => (
                  <TextField
                    {...field}
                    select
                    fullWidth
                    error={!!fieldState.error}
                    helperText={fieldState.error?.message}
                  >
                    {brands?.map((opt: BrandInterface) => (
                      <MenuItem key={opt.id} value={opt.id}>
                        {opt.name} {`( ${opt.code})`}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
            <Grid sx={{ mt: 2.5 }}>
              <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
                Tipo de Contenido *
              </Typography>
              <Controller
                name="content_type"
                control={control}
                render={({ field, fieldState }) => (
                  <TextField
                    {...field}
                    select
                    fullWidth
                    error={!!fieldState.error}
                    helperText={fieldState.error?.message}
                  >
                    {CONTENT_TYPE_OPTIONS.map((opt) => (
                      <MenuItem key={opt.value} value={opt.value}>
                        {opt.label}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>

            <Grid sx={{ mt: 2.5 }}>
              <Controller
                name="user_prompt"
                control={control}
                render={({ field, fieldState }) => (
                  <TextField
                    {...field}
                    multiline
                    rows={4}
                    sx={{
                      "& .MuiOutlinedInput-root": {
                        minHeight: "48px",
                        height: "auto",
                        p: "10px 14px",
                      },
                      "& .MuiOutlinedInput-input": { p: 0 },
                    }}
                    fullWidth
                    placeholder="Describe el contenido..."
                    error={!!fieldState.error}
                    helperText={fieldState.error?.message}
                  />
                )}
              />
            </Grid>
            {/* Panel de Auditoría / Sugerencias */}
            {audit && (
              <Grid sx={{ mt: 2.5 }}>
                <Alert
                  severity={audit.severity === "HIGH" ? "error" : "warning"}
                  action={
                    audit.improved_prompt && (
                      <Button
                        color="inherit"
                        size="small"
                        onClick={handleApplyImprovement}
                        startIcon={<AutoFixHighIcon />}
                      >
                        Aplicar Mejora
                      </Button>
                    )
                  }
                >
                  <Typography variant="subtitle2">
                    Auditoríadel sistema:
                  </Typography>
                  <ul style={{ margin: 0, paddingLeft: "20px" }}>
                    {audit.feedback.map((f: string, i: number) => (
                      <li key={i}>{f}</li>
                    ))}
                  </ul>
                </Alert>
              </Grid>
            )}

            {generatedLog && (
              <>
                {generatedLog.content_data?.is_aligned === false && (
                  <Alert severity="info" sx={{ mt: 2, mb: 1 }}>
                    <Typography
                      variant="caption"
                      fontWeight="bold"
                      display="block"
                    >
                      Nota del Motor Creativo:
                    </Typography>
                    <Typography variant="caption">
                      {generatedLog.content_data?.llm_opinion}
                    </Typography>
                  </Alert>
                )}

                <Box
                  sx={{
                    p: 2,
                    bgcolor: "grey.50",
                    borderRadius: 2,
                    border: "1px solid #e0e0e0",
                    position: "relative",
                    mt: 1,
                  }}
                >
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      mb: 1,
                    }}
                  >
                    <Typography
                      sx={{
                        color: "gray",
                        fontSize: "10px",
                        fontWeight: "bold",
                      }}
                    >
                      CONTENIDO GENERADO
                    </Typography>
                    <Stack direction="row" spacing={0.5}>
                      <IconButton
                        size="small"
                        onClick={handleCopy}
                        title="Copiar"
                      >
                        <IconCopy size={16} />
                      </IconButton>
                      {generatedLog?.status === "CREATED" && (
                        <IconButton
                          size="small"
                          onClick={handleOpenConfirmCambiarStatus}
                          title="Solicitar auditoría humana"
                          color="primary"
                        >
                          <IconBellRinging size={16} />
                        </IconButton>
                      )}
                    </Stack>
                  </Box>
                  <Typography
                    variant="body2"
                    sx={{ whiteSpace: "pre-line", color: "text.primary" }}
                  >
                    {generatedLog.content_data?.text ||
                      generatedLog.content_data?.generated_content}
                  </Typography>
                </Box>
              </>
            )}
          </Box>
        </DialogContent>

        <DialogActions
          sx={{
            p: 3,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 1.5,
          }}
        >
          <Button
            onClick={handleClose}
            color="inherit"
            variant="outlined"
            sx={{ textTransform: "none", minWidth: "100px" }}
          >
            Cancelar
          </Button>
          <Button
            onClick={handleSubmit(handleGenerate)}
            sx={{ textTransform: "none", minWidth: "100px" }}
            variant="contained"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="loadingBtn">
                <CircularProgress size={20} style={{ color: "#FFFFFF" }} />
              </div>
            ) : (
              <>
                {generatedLog
                  ? "Ajustar"
                  : audit
                    ? "Reintentar con ajuste"
                    : "Generar"}
              </>
            )}
          </Button>
        </DialogActions>
      </Dialog>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={2000}
        onClose={() => setSnackbarOpen(false)}
        message="Texto copiado al portapapeles"
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      />
      {generatedLog?.id && isConfirmCambiarStatusOpen && (
        <ConfirmActionModal
          open={isConfirmCambiarStatusOpen}
          onClose={handleCloseConfirmCambiarStatus}
          handleConfirm={() => handleConfirm(generatedLog.id)}
          title={auditarRequestTitle}
          description={auditarRequestQuestion}
          loading={isLoading}
        />
      )}
    </>
  );
};
