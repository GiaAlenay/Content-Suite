// src/common/utils/schemas.ts (Añade esto a tus schemas existentes)
import { z } from 'zod';

export const GenerateManualSchema = z.object({
  mission: z.string().min(10, "La misión debe tener al menos 10 caracteres"),
  tone: z.string().min(5, "Describe el tono de voz (ej: Formal, Amigable)"),
  rules: z.string().min(10, "Define al menos una regla clara de comunicación"),
  visual_identity: z.string().min(10, "Describe brevemente los elementos visuales clave"),
});

export type GenerateManualInputs = z.infer<typeof GenerateManualSchema>;