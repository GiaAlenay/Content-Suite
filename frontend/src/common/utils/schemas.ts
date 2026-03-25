import { z } from 'zod';

export const LoginSchema = z.object({
  email: z
    .string()
    .min(1, "El email es requerido")
    .email("Formato de email inválido"),
  password: z
    .string()
    .min(6, "La contraseña debe tener al menos 6 caracteres"),
});

export type LoginFormInputs = z.infer<typeof LoginSchema>;