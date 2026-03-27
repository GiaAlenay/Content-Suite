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
  const [isLoading, setIsLoading] = useState(false);
  const [generatedManualText, setGeneratedManualText] = useState<string | null>(
    null,
  );
  const [copied, setCopied] = useState(false);

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
    setCopied(false);
    onClose();
  };

  const onSubmit = async (data: GenerateManualInputs) => {
    setIsLoading(true);
    setGeneratedManualText(null);
    console.log("Datos enviados a la IA:", data);

    await new Promise((resolve) => setTimeout(resolve, 2000));

    const mockApiResponse = `
# MANUAL DE MARCA: ${brandName.toUpperCase()}

## 1. MISIÓN DE LA IA
${data.mission} (Refinado por la IA para máxima claridad operativa)

## 2. TONO DE VOZ
Nuestra comunicación debe ser ${data.tone}. Evitar tecnicismos innecesarios.

## 3. REGLAS CRÍTICAS
- ${data.rules}
- Mantener consistencia en todas las plataformas.

## 4. IDENTIDAD VISUAL
Los elementos visuales clave son: ${data.visual_identity}.

Este manual es una guía operativa para la generación de contenido.
    `;

    setGeneratedManualText(mockApiResponse.trim());
    setIsLoading(false);
  };

  const handleCopy = () => {
    if (generatedManualText) {
      navigator.clipboard.writeText(generatedManualText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); // Reset icono copiado
    }
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
              disabled={isLoading}
              placeholder="Ej: Automatizar procesos legales complejos para startups..."
            />
          </Grid>
          <Grid>
            <ManualSectionField
              name="tone"
              label="Tono de Voz"
              control={control}
              errors={errors}
              disabled={isLoading}
              placeholder="Ej: Profesional pero accesible, directo, usar 'nosotros'..."
            />
          </Grid>
          <Grid>
            <ManualSectionField
              name="rules"
              label="Reglas de Comunicación"
              control={control}
              errors={errors}
              disabled={isLoading}
              placeholder="Ej: Nunca prometer resultados legales específicos. Siempre citar fuentes..."
            />
          </Grid>
          <Grid>
            <ManualSectionField
              name="visual_identity"
              label="Identidad Visual "
              control={control}
              errors={errors}
              disabled={isLoading}
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

        {/* Sección 2: Display del Resultado (Solo lectura con Copiar) */}
        {generatedManualText && (
          <Box sx={{ mt: 2, borderTop: "2px dashed #e0e0e0", pt: 3 }}>
            <Stack
              direction="row"
              justifyContent="space-between"
              alignItems="center"
              sx={{ mb: 1.5 }}
            >
              <Typography variant="h6" fontWeight="600" color="primary">
                Manual Generado (Solo Lectura)
              </Typography>
              <Tooltip title={copied ? "¡Copiado!" : "Copiar al portapapeles"}>
                <Button
                  variant="outlined"
                  startIcon={
                    copied ? (
                      <IconCheck size={20} color="green" />
                    ) : (
                      <IconCopy size={20} />
                    )
                  }
                  onClick={handleCopy}
                  color={copied ? "success" : "primary"}
                  sx={{ textTransform: "none", borderRadius: "8px" }}
                >
                  {copied ? "Copiado" : "Copiar Texto"}
                </Button>
              </Tooltip>
            </Stack>

            <TextField
              fullWidth
              multiline
              rows={12}
              value={generatedManualText}
              InputProps={{ readOnly: true }}
              sx={{
                bgcolor: "#f8f9fa", // Fondo gris muy claro para diferenciar
                borderRadius: "8px",
                "& .MuiOutlinedInput-notchedOutline": {
                  borderColor: "#e0e0e0",
                },
                "& .MuiInputBase-input": {
                  fontFamily: "monospace", // Estilo código para manuales
                  fontSize: "0.9rem",
                  color: "text.primary",
                },
              }}
            />
          </Box>
        )}
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
            // startIcon={isLoading ? null : <IconWand size={20} />}
            disabled={isLoading}
            sx={{}} // Hereda color global
          >
            {isLoading ? "Procesando con IA..." : "Generar"}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};
