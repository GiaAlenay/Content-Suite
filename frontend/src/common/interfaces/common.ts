import type { User, Session } from '@supabase/supabase-js';
import type { LoginFormInputs } from '../utils/schemas';

export type Order = "asc" | "desc";
export interface TableColumn {
  id: string;          // El identificador único (ej: "logo_url", "name")
  label: string;       // El texto que se mostrará en el encabezado
  numeric: boolean;    // Si el contenido debe alinearse a la derecha
  disablePadding: boolean;
  maxwidth?: string;   // Opcional, ya que no todas las columnas podrían necesitarlo
}

// src/common/types/api.types.ts

export interface ApiResponseSuccess<T> {
  success: boolean;
  message: string;
  data: T; // Aquí T será el listado de Brands, un objeto User, etc.
}

export interface ApiResponseError {
  success: boolean;
  message: string;
}

export interface AuthContextType {
  user: User | null;
  session: Session | null;
  loading: boolean;
  signIn: (data: LoginFormInputs) => Promise<void>;
  signOut: () => Promise<void>;
}