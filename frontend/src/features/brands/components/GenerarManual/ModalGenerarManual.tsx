// src/features/brands/components/GenerateManualModal.tsx
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  TextField,
  Stack,
  IconButton,
  Tooltip,
  Alert,
} from "@mui/material";
import { Grid } from "@mui/material";

import { IconCopy, IconCheck, IconX } from "@tabler/icons-react";
import {
  GenerateManualSchema,
  type GenerateManualInputs,
} from "../../schemas/generarManual";
import { ManualSectionField } from "./ManualSectionField";
import { useManualGenerator } from "../../hooks/useBrands copy";

interface GenerateManualModalProps {
  open: boolean;
  onClose: () => void;
  brandName: string;
}

export const GenerateManualModal = ({
  open,
  onClose,
  brandName,
}: GenerateManualModalProps) => {
  const { auditManual, isAuditing } = useManualGenerator();
  const [generatedManualText, setGeneratedManualText] = useState<string | null>(
    null,
  );

  const {
    control,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<GenerateManualInputs>({
    resolver: zodResolver(GenerateManualSchema),
    defaultValues: { mission: "", tone: "", rules: "", visual_identity: "" },
  });

  const handleClose = () => {
    reset();
    setGeneratedManualText(null);
    onClose();
  };

  const onSubmit = async (data: GenerateManualInputs) => {
    console.log(data);
  };

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
      <DialogTitle
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
          fontWeight: "bold",
        }}
      >
        <Typography variant="h6" fontWeight="bold">
          Generar Manual para {brandName}
        </Typography>
        <IconButton onClick={handleClose} sx={{ ml: "auto" }} size="small">
          <IconX size={20} />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers sx={{ p: 3 }}>
        {/* Sección 1: Formulario de Entrada */}
        <Box
          component="form"
          onSubmit={handleSubmit(onSubmit)}
          sx={{ mb: generatedManualText ? 4 : 0 }}
        >
          <Grid>
            <ManualSectionField
              name="mission"
              label="Misión de la Marca"
              control={control}
              errors={errors}
              disabled={isAuditing}
              placeholder="Ej: Automatizar procesos legales complejos para startups..."
            />
          </Grid>
          <Grid>
            <ManualSectionField
              name="tone"
              label="Tono de Voz"
              control={control}
              errors={errors}
              disabled={isAuditing}
              placeholder="Ej: Profesional pero accesible, directo, usar 'nosotros'..."
            />
          </Grid>
          <Grid>
            <ManualSectionField
              name="rules"
              label="Reglas de Comunicación"
              control={control}
              errors={errors}
              disabled={isAuditing}
              placeholder="Ej: Nunca prometer resultados legales específicos. Siempre citar fuentes..."
            />
          </Grid>
          <Grid>
            <ManualSectionField
              name="visual_identity"
              label="Identidad Visual "
              control={control}
              errors={errors}
              disabled={isAuditing}
              placeholder="Ej: Paleta azul cobalto (#0047AB) y blanco absoluto. Tipografía Sans-Serif moderna..."
            />
          </Grid>

          {!generatedManualText && (
            <Alert severity="info" sx={{ mt: 2, borderRadius: "8px" }}>
              Al hacer clic en 'Generar', la IA procesará esta información para
              estructurar el manual final.
            </Alert>
          )}
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 2.5, justifyContent: "flex-end", gap: 1.5 }}>
        <Button onClick={handleClose} variant="outlined">
          {generatedManualText ? "Cerrar" : "Cancelar"}
        </Button>

        {/* Botón Principal (Naranja Global) */}
        {!generatedManualText && (
          <Button
            onClick={handleSubmit(onSubmit)}
            variant="contained"
            // startIcon={isAuditing ? null : <IconWand size={20} />}
            disabled={isAuditing}
            sx={{}} // Hereda color global
          >
            {isAuditing ? "Procesando con IA..." : "Generar"}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};
