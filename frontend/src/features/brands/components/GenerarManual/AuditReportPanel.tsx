import {
  Box,
  Typography,
  Alert,
  AlertTitle,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import { IconAlertTriangle, IconInfoCircle } from "@tabler/icons-react";
import type { AuditManualResponse } from "../../interfaces/ManualGeneratorData";

export const AuditReportPanel = ({
  report,
}: {
  report: AuditManualResponse;
}) => {
  const isHigh = report.severity === "HIGH";

  return (
    <Box sx={{ p: 2 }}>
      <Typography
        variant="h6"
        fontWeight="bold"
        gutterBottom
        color={isHigh ? "error.main" : "warning.main"}
      >
        Reporte de Coherenciadel sistema
      </Typography>

      <Alert
        severity={isHigh ? "error" : "warning"}
        icon={<IconAlertTriangle />}
        sx={{ mb: 3, borderRadius: 2 }}
      >
        <AlertTitle>
          {isHigh ? "Bloqueo por Incoherencia" : "Sugerencias de Mejora"}
        </AlertTitle>
        {isHigh
          ? "Se han detectado conflictos críticos que impiden la generación de un manual profesional."
          : "Nuestro sistema ha detectado áreas que podrían confundir a la audiencia."}
      </Alert>

      <Typography variant="subtitle1" fontWeight="bold" sx={{ mt: 2 }}>
        Conflictos detectados:
      </Typography>
      <List
        sx={{
          minHeight: "auto",
          maxHeight: 500,
          overflowY: "auto",
        }}
      >
        {report.feedback.map((msg, index) => (
          <ListItem key={index} sx={{ px: 0 }}>
            <ListItemIcon sx={{ minWidth: 35 }}>
              <IconInfoCircle size={20} color="#666" />
            </ListItemIcon>
            <ListItemText primary={msg} />
          </ListItem>
        ))}
      </List>

      <Box
        sx={{
          mt: 3,
          p: 2,
          bgcolor: "white",
          borderRadius: 2,
          borderLeft: "4px solid",
          borderColor: "primary.main",
        }}
      >
        <Typography
          variant="subtitle2"
          color="primary"
          fontWeight="bold"
          gutterBottom
        >
          Sugerencia de la IA para corregir:
        </Typography>
        <Typography variant="body2" italic>
          "{report.suggestions}"
        </Typography>
      </Box>
    </Box>
  );
};
