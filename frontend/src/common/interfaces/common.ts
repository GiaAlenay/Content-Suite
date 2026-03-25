export type Order = "asc" | "desc";
export interface TableColumn {
  id: string;          // El identificador único (ej: "logo_url", "name")
  label: string;       // El texto que se mostrará en el encabezado
  numeric: boolean;    // Si el contenido debe alinearse a la derecha
  disablePadding: boolean;
  maxwidth?: string;   // Opcional, ya que no todas las columnas podrían necesitarlo
}