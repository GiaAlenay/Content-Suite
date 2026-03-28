// src/common/utils/schemas.ts (Añade esto a tus schemas existentes)
import { z } from 'zod';

export const GenerateManualSchema = z.object({
  target_audience: z.string().min(5, "La audiencia debe ser más descriptiva"),
  core_values: z.array(z.string()).min(1, "Selecciona al menos un valor nuclear"),
  tone_preference: z.string().min(3, "El tono es obligatorio (ej: Cercano, motivador)"),
  forbidden_topics: z.array(z.string()).default([]),
  additional_notes: z.string().optional(),
  brand_colors: z.array(z.string()).min(1, "Define al menos un color (ej: #0047AB)"),
  visual_style: z.string().min(10, "Describe el estilo visual (ej: Minimalista)"),
  logo_guidelines: z.string().optional(),
});

export type GenerateManualInputs = z.infer<typeof GenerateManualSchema>;