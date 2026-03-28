import { Stack, Typography, Box } from "@mui/material";
import { IconSparkles } from "@tabler/icons-react";

export const EmptyStateIA = () => {
  return (
    <Stack
      spacing={3}
      alignItems="center"
      justifyContent="center"
      sx={{ height: "100%", opacity: 0.6, textAlign: "center", p: 4 }}
    >
      <Box
        sx={{
          width: 80,
          height: 80,
          borderRadius: "50%",
          bgcolor: "primary.light",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "primary.main",
        }}
      >
        <IconSparkles size={40} />
      </Box>
      <Box>
        <Typography variant="h5" fontWeight="bold" gutterBottom>
          Listo para construir tu marca
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Completa los pasos del formulario a la izquierda. <br />
          Nuestro Agente de Gobernanza auditará tus inputs para asegurar la
          coherencia estratégica.
        </Typography>
      </Box>
    </Stack>
  );
};
