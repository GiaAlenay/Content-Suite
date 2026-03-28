import { useState, useMemo } from "react";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import { IconSend } from "@tabler/icons-react";
import ReactMarkdown from "react-markdown";
import type { ManualRecord } from "../../interfaces/ManualGeneratorData";
import SettingsIcon from "@mui/icons-material/Settings";
import { keyframes } from "@mui/system";

const rotate = keyframes`
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
`;

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
    setRefinePrompt("");
  };

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
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="h6" fontWeight="bold">
          Borrador (v{manual.version})
        </Typography>
        <Button
          variant="outlined"
          color="success"
          onClick={onConfirm}
          disabled={isConfirming || isRefining}
          sx={{ textTransform: "none", minWidth: "100px" }}
        >
          Aprobar
        </Button>
      </Stack>

      <Paper
        elevation={3}
        sx={{
          flex: 1,
          overflowY: "auto",
          borderRadius: 2,
          bgcolor: "white",
          border: "1px solid #e0e0e0",
          padding: "24px",
        }}
      >
        {isRefining ? (
          <Stack
            alignItems="center"
            justifyContent="center"
            sx={{
              height: "100%",
              bgcolor: "rgba(255,255,255,0.7)",
              textAlign: "center",
            }}
          >
            <SettingsIcon
              sx={{
                fontSize: 50,
                color: "gray",
                animation: `${rotate} 2s linear infinite`,
              }}
            />
            <Typography
              sx={{ mt: 2, fontWeight: 500, color: "text.secondary" }}
            >
              Refinando detalles...
            </Typography>
          </Stack>
        ) : (
          MarkdownViewer
        )}
      </Paper>

      <Paper
        elevation={4}
        sx={{
          p: 2,
          borderRadius: 3,
          border: "1px solid b",
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
            InputProps={{ disableUnderline: true }}
          />
          <Button
            onClick={handleRefineSubmit}
            disabled={!refinePrompt.trim() || isRefining || isConfirming}
            sx={{
              borderRadius: 2,
              minWidth: 48,
              height: 48,
              p: 0,
              color: "rgba(121, 121, 121, 0.87)",
            }}
          >
            <IconSend size={24} />
          </Button>
        </Stack>
      </Paper>

      <Typography variant="caption" sx={{ color: "gray" }} textAlign="center">
        Versión actual: {new Date(manual.created_at || "").toLocaleString()}
      </Typography>
    </Box>
  );
};
