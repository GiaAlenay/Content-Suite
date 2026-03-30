import { z } from "zod";

export const GenerateContentSchema = z.object({
  brand_id: z.string().min(1, "Selecciona una marca"),
  content_type: z.string().min(1, "Selecciona el tipo de contenido"),
  user_prompt: z
    .string()
    .min(10, "El prompt debe ser más descriptivo (min. 10 caracteres)"),
  parent_log_id: z.string().optional().nullable(),
});

export type GenerateContentInputs = z.infer<typeof GenerateContentSchema>;
