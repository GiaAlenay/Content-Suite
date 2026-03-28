import { Stack, Typography, TextField, Grid } from "@mui/material";
import { useFormContext, Controller } from "react-hook-form";
import { TagInput } from "../../../../../common/components/TagInput";

export const StrategicSection = () => {
  const {
    control,
    formState: { errors },
  } = useFormContext();

  return (
    <Stack spacing={3}>
      <Typography variant="h6" fontWeight="bold">
        Estrategia de Marca
      </Typography>

      <Grid sx={{ mt: 2.5 }}>
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
          Audiencia Objetivo *
        </Typography>
        <Controller
          name="target_audience"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              placeholder="Ej: Emprendedores tecnológicos de 25-40 años"
              error={!!errors.target_audience}
              helperText={errors.target_audience?.message as string}
            />
          )}
        />
      </Grid>

      <Grid sx={{ mt: 2.5 }}>
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
          Valores Principales *
        </Typography>
        <Controller
          name="core_values"
          control={control}
          render={({ field }) => (
            <TagInput
              placeholder="Escribe un valor y presiona Enter"
              tags={field.value || []}
              onChange={field.onChange}
              error={!!errors.core_values}
            />
          )}
        />
      </Grid>

      <Grid sx={{ mt: 2.5 }}>
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
          Preferencia de Tono *
        </Typography>
        <Controller
          name="tone_preference"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              placeholder="Ej: Cercano, inspirador y altamente técnico"
              fullWidth
              multiline
              rows={4}
              error={!!errors.tone_preference}
              helperText={errors.tone_preference?.message as string}
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
