import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Stack,
  Divider,
  Box,
} from "@mui/material";
import type { ContentLogTableData } from "../interfaces/ContentLogData";
import { formatDateToSpanish } from "../../../common/utils/timeTransformer";

interface Props {
  open: boolean;
  onClose: () => void;
  contentLog: ContentLogTableData | null;
}

export const ContentLogDetailModal: React.FC<Props> = ({
  open,
  onClose,
  contentLog,
}) => {
  if (!contentLog) return null;

  const renderTag = (status: string) => {
    if (status === "CREATED")
      return <div className="tag-item-estado tag-inactive">Creado</div>;
    if (status === "PENDING")
      return <div className="tag-item-estado tag-pending">Pendiente</div>;
    if (status === "APPROVED")
      return <div className="tag-item-estado tag-approved">Aprovado</div>;
    return <div className="tag-item-estado tag-rejected">Rechazado</div>;
  };
  const renderCode = () => {
    return ` (${contentLog.brand_code})`;
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 1.5,
          fontWeight: "bold",
        }}
      >
        <Typography variant="h6" fontWeight="bold" component="span">
          Detalles
        </Typography>
        <Box>{renderTag(contentLog.status)}</Box>
      </DialogTitle>

      <DialogContent dividers>
        <Stack spacing={2.5}>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Marca
            </Typography>
            <Typography variant="body1" fontWeight="500">
              {contentLog.brand_name}
              <span style={{ color: "#666" }}>{renderCode()}</span>
            </Typography>
          </Box>

          <Stack direction="row" justifyContent="space-between">
            <Box>
              <Typography variant="caption" color="text.secondary">
                Tipo de contenido
              </Typography>
              <Typography variant="body1">{contentLog.content_type}</Typography>
            </Box>
          </Stack>

          <Box>
            <Typography variant="caption" color="text.secondary">
              Fecha de creación
            </Typography>
            <Typography variant="body1">
              {formatDateToSpanish(contentLog.created_at)}
            </Typography>
          </Box>

          <Divider />

          <Box>
            <Typography variant="caption" color="text.secondary">
              Auditado por
            </Typography>
            <Typography variant="body1">
              {contentLog.audit_by ?? "-"}
            </Typography>
          </Box>

          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: "block", mb: 0.5 }}
            >
              Retroalimentación del Agente
            </Typography>
            <Typography
              variant="body2"
              sx={{
                p: 2,
                bgcolor: "#f5f5f5",
                borderRadius: 1,
                fontStyle: contentLog.agent_feedback ? "normal" : "italic",
              }}
            >
              {contentLog.agent_feedback ?? "Sin retroalimentación disponible."}
            </Typography>
          </Box>

          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: "block", mb: 0.5 }}
            >
              Prompt
            </Typography>
            <Box
              sx={{
                p: 2,
                borderRadius: 1,
                overflowY: "auto",
                whiteSpace: "pre-wrap",
              }}
            >
              <Typography variant="body2">
                {contentLog.prompt_origin}
              </Typography>
            </Box>
          </Box>

          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: "block", mb: 0.5 }}
            >
              Contenido Generado
            </Typography>
            <Box
              sx={{
                p: 2,
                border: "1px solid #e0e0e0",
                borderRadius: 1,
                maxHeight: "200px",
                overflowY: "auto",
                whiteSpace: "pre-wrap",
              }}
            >
              <Typography variant="body2">
                {contentLog.content_data?.text
                  ? contentLog.content_data?.text
                  : contentLog.content_data?.generated_content
                    ? contentLog.content_data?.generated_content
                    : "No hay texto disponible."}
              </Typography>
            </Box>
          </Box>
        </Stack>
      </DialogContent>

      <DialogActions sx={{ p: 2 }}>
        <Button onClick={onClose} variant="outlined" color="primary">
          Cerrar
        </Button>
      </DialogActions>
    </Dialog>
  );
};
