import { z } from "zod";

const spanishErrorMap: any = (issue: any, ctx: any) => {
  // 1. Verificamos que ctx exista para evitar el TypeError
  const defaultMsg = ctx?.defaultError ?? "Dato inválido";
  
  // 2. Extraemos el código de forma segura
  const code = issue.code;

  // 3. Mapeo de errores basándonos en tu log de consola
if (code === "invalid_type") {
    // Si no recibimos nada, o si explícitamente dice que recibió undefined/null
    if (!issue.received || issue.received === "undefined" || issue.received === "null") {
      return { message: "Este campo es obligatorio" };
    }
    
    // Traducción para tipos de datos (opcional)
    const received = issue.received === "number" ? "un número" : issue.received;
    return { message: `Se esperaba un texto, pero recibimos ${received}` };
  }

  if (code === "too_small") {
    if (issue.type === "string") {
      return { message: `Debe tener al menos ${issue.minimum} caracteres` };
    }
    if (issue.type === "array") {
      return { message: "Selecciona al menos un elemento" };
    }
  }

  if (code === "invalid_string") {
    if (issue.validation === "email" || issue.kind === "email") {
      return { message: "El formato del correo no es válido" };
    }
  }

  // 4. Si no coincide con nada, devolvemos el default de forma segura
  return { message: defaultMsg };
};

export const initZodSpanish = () => {
  z.setErrorMap(spanishErrorMap);
};