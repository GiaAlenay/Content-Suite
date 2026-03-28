import { useState, useMemo } from "react";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Stack,
  CircularProgress,
} from "@mui/material";
import { IconSend, IconFileCheck } from "@tabler/icons-react";
import ReactMarkdown from "react-markdown";
import type { ManualRecord } from "../../interfaces/ManualGeneratorData";
interface ManualWorkspaceProps {
  manual: ManualRecord;
  onRefine: (prompt: string) => Promise<void>;
  onConfirm: () => Promise<void>;
  isRefining: boolean;
  isConfirming: boolean;
}

export const ManualWorkspace = ({
  manual,
  onRefine,
  onConfirm,
  isRefining,
  isConfirming,
}: ManualWorkspaceProps) => {
  const [refinePrompt, setRefinePrompt] = useState("");

  const handleRefineSubmit = async () => {
    if (!refinePrompt.trim()) return;
    await onRefine(refinePrompt);
    setRefinePrompt(""); // Limpiar tras éxito
  };

  // Memorizamos el visor para que no se re-procese el Markdown si solo cambia el texto del input
  const MarkdownViewer = useMemo(
    () => (
      <Box
        className="markdown-body"
        sx={{ p: 4, color: "#333", lineHeight: 1.7 }}
      >
        <ReactMarkdown>{manual.full_manual}</ReactMarkdown>
      </Box>
    ),
    [manual.full_manual],
  );

  return (
    <Box
      sx={{ display: "flex", flexDirection: "column", height: "100%", gap: 2 }}
    >
      {/* Cabecera del Workspace */}
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="h6" fontWeight="bold">
          Borrador del Manual (v{manual.version})
        </Typography>
        <Button
          variant="contained"
          color="success"
          startIcon={
            isConfirming ? (
              <CircularProgress size={20} color="inherit" />
            ) : (
              <IconFileCheck size={20} />
            )
          }
          onClick={onConfirm}
          disabled={isConfirming || isRefining}
        >
          Confirmar y Generar PDF
        </Button>
      </Stack>

      {/* Visor de Documento (Efecto Papel) */}
      <Paper
        elevation={3}
        sx={{
          flex: 1,
          overflowY: "auto",
          borderRadius: 2,
          bgcolor: "white",
          border: "1px solid #e0e0e0",
        }}
      >
        {isRefining ? (
          <Stack
            alignItems="center"
            justifyContent="center"
            sx={{ height: "100%", bgcolor: "rgba(255,255,255,0.7)" }}
          >
            <CircularProgress size={40} />
            <Typography sx={{ mt: 2 }}>Refinando con IA...</Typography>
          </Stack>
        ) : (
          MarkdownViewer
        )}
      </Paper>

      {/* Panel de Refinamiento (Chat Bar) */}
      <Paper
        elevation={4}
        sx={{
          p: 2,
          borderRadius: 3,
          border: "1px solid",
          borderColor: "primary.light",
        }}
      >
        <Stack direction="row" spacing={2} alignItems="flex-end">
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder="¿Quieres ajustar algo? Ej: 'Haz que la misión suene más épica' o 'Cambia el azul por uno más oscuro'..."
            value={refinePrompt}
            onChange={(e) => setRefinePrompt(e.target.value)}
            disabled={isRefining}
            variant="standard"
            InputProps={{ disableUnderline: true, sx: { px: 1 } }}
          />
          <Button
            variant="contained"
            onClick={handleRefineSubmit}
            disabled={!refinePrompt.trim() || isRefining}
            sx={{ borderRadius: 2, minWidth: 48, height: 48, p: 0 }}
          >
            <IconSend size={24} />
          </Button>
        </Stack>
      </Paper>

      <Typography variant="caption" color="text.secondary" textAlign="center">
        Versión actual: {new Date(manual.created_at || "").toLocaleString()}
      </Typography>
    </Box>
  );
};
