
import { z } from "zod";

export const CreateBrandSchema = z.object({
  code: z.string().min(3, "Mínimo 3 caracteres").max(50, "Máximo 50"),
  name: z.string().min(2, "El nombre es requerido").max(100),
  description: z.string().max(255, "Máximo 255 caracteres").optional().or(z.literal('')),
  logo_url: z.string().url("Debe ser una URL válida").optional().or(z.literal('')),
});

export type CreateBrandInputs = z.infer<typeof CreateBrandSchema>;