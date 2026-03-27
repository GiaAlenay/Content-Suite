import { Box, Typography } from "@mui/material";
import { IconSearchOff } from "@tabler/icons-react";

export const NoFilteredData = ({ itemsName }: { itemsName: string }) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        py: 10,
        borderRadius: 2,
        border: "1px dashed #ccc",
      }}
    >
      <IconSearchOff size={48} color="#9e9e9e" />
      <Typography variant="h6" color="text.secondary" sx={{ mt: 2 }}>
        No se encontraron {itemsName}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Prueba ajustando los filtros o el término de búsqueda.
      </Typography>
    </Box>
  );
};
