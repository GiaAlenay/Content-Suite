import { z } from "zod";

export const GenerateContentSchema = z.object({
  user_prompt: z
    .string()
    .min(
      10,
      "Por favor, describe mejor lo que necesitas (mínimo 10 caracteres)",
    )
    .max(2000, "El prompt es demasiado largo"),

  content_type: z.string().min(1, "Debes seleccionar un tipo de contenido"),
});

export type GenerateContentInputs = z.infer<typeof GenerateContentSchema>;
