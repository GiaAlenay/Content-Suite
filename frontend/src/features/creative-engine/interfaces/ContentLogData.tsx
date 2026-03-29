// Definimos los estados posibles para mayor seguridad en el tipado
export type ContentStatus = "PENDING" | "APPROVED" | "REJECTED";

export interface ContentLogInterface {
  id?: string;
  brand_id: string;
  brand_code: string;
  brand_name: string;
  creator_id: string;
  content_data: Record<string, string>;
  content_type: string;
  status: ContentStatus;
  agent_feedback?: string | null;
  audit_by?: string | null;
  prompt_origin?: string | null;

  created_at?: string;
  updated_at?: string;
}

export interface ContentLogTableData {
  id?: string;
  brand_id: string;
  brand_code: string;
  brand_name: string;
  creator_id: string;
  content_data: Record<string, string>;
  content_type: string;
  status: ContentStatus;
  agent_feedback?: string | null;
  audit_by?: string | null;
  prompt_origin?: string | null;
}
