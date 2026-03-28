import {
  Stack,
  Typography,
  TextField,
  Button,
  Collapse,
  Grid,
} from "@mui/material";
import { useFormContext, Controller } from "react-hook-form";
import { useState } from "react";
import { TagInput } from "../../../../../common/components/TagInput";
import { IconPlus } from "@tabler/icons-react";

export const AdditionalSection = () => {
  const { control } = useFormContext();
  const [showNotes, setShowNotes] = useState(false);

  return (
    <Stack spacing={3}>
      <Typography variant="h6" fontWeight="bold">
        Notas y Restricciones
      </Typography>

      <Controller
        name="forbidden_topics"
        control={control}
        render={({ field }) => (
          <TagInput
            placeholder="Ej: Política, Criptomonedas, Competencia (presiona Enter)"
            tags={field.value || []}
            onChange={field.onChange}
            color="error"
          />
        )}
      />

      {!showNotes && (
        <Button
          startIcon={<IconPlus size={18} />}
          onClick={() => setShowNotes(true)}
          sx={{ alignSelf: "flex-start" }}
        >
          Agregar notas adicionales
        </Button>
      )}

      <Collapse in={showNotes}>
        <Grid sx={{ mt: 2.5 }}>
          <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
            Instrucciones adicionales
          </Typography>
          <Controller
            name="additional_notes"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                placeholder="Ej: Enfócate mucho en la sección de LinkedIn..."
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
      </Collapse>
    </Stack>
  );
};
