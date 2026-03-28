import { Stack, Typography, TextField, Grid } from "@mui/material";
import { useFormContext, Controller } from "react-hook-form";
import { ColorChipInput } from "../../../../../common/components/ColorChipInput";

export const VisualSection = () => {
  const {
    control,
    formState: { errors },
  } = useFormContext();

  return (
    <Stack spacing={3}>
      <Typography variant="h6" fontWeight="bold">
        Identidad Visual
      </Typography>

      <Grid sx={{ mt: 2.5 }}>
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
          Paleta de Colores (HEX) *
        </Typography>
        <Controller
          name="brand_colors"
          control={control}
          render={({ field }) => (
            <ColorChipInput
              colors={field.value || []}
              onChange={field.onChange}
              error={!!errors.brand_colors}
            />
          )}
        />
      </Grid>

      <Grid sx={{ mt: 2.5 }}>
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
          Estilo Visual General *
        </Typography>
        <Controller
          name="visual_style"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              placeholder="Ej: Minimalista, estilo suizo, mucho espacio en blanco"
              fullWidth
              multiline
              rows={4}
              error={!!errors.visual_style}
              helperText={errors.visual_style?.message as string}
              sx={{
                "& .MuiOutlinedInput-root": {
                  minHeight: "48px",
                  height: "auto",
                  p: "10px 14px",
                },
                "& .MuiOutlinedInput-input": { p: 0 },
              }}
            />
          )}
        />
      </Grid>

      <Grid sx={{ mt: 2.5 }}>
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
          Lineamientos del Logo
        </Typography>
        <Controller
          name="logo_guidelines"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              placeholder="Ej: No usar sobre fondos oscuros, mantener área de respeto..."
              fullWidth
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
            />
          )}
        />
      </Grid>
    </Stack>
  );
};
