// src/features/brands/components/ManualSectionField.tsx
import { Controller } from "react-hook-form";
import type { Control, FieldErrors } from "react-hook-form";
import { Box, Typography, TextField, FormHelperText } from "@mui/material";
import type { GenerateManualInputs } from "../../schemas/generarManual";

interface ManualSectionFieldProps {
  name: keyof GenerateManualInputs;
  label: string;
  placeholder: string;
  control: Control<GenerateManualInputs>;
  errors: FieldErrors<GenerateManualInputs>;
  disabled?: boolean;
}

export const ManualSectionField = ({
  name,
  label,
  placeholder,
  control,
  errors,
  disabled,
}: ManualSectionFieldProps) => {
  return (
    <Box sx={{ mb: 2 }}>
      <Typography
        variant="body2"
        sx={{ fontWeight: 600, mb: 0.5, color: "text.primary" }}
      >
        {label} *
      </Typography>

      <Controller
        name={name}
        control={control}
        render={({ field }) => (
          <TextField
            {...field}
            fullWidth
            multiline
            rows={3} // Altura inicial para TextAreas
            placeholder={placeholder}
            error={!!errors[name]}
            disabled={disabled}
            // Mantenemos la estética global de 48px, pero dejamos crecer el TextArea
            sx={{
              "& .MuiOutlinedInput-root": {
                minHeight: "48px", // Mínimo de tu diseño
                height: "auto", // Permite que multiline crezca
                p: "10px 14px", // Padding consistente
              },
              "& .MuiOutlinedInput-input": { p: 0 }, // Reset del padding interno del textarea
            }}
          />
        )}
      />
      {errors[name] && (
        <FormHelperText error sx={{ mx: 0 }}>
          {errors[name]?.message}
        </FormHelperText>
      )}
    </Box>
  );
};
