// Definimos los estados posibles para mayor seguridad en el tipado
export type ContentStatus = "CREATED" | "PENDING" | "APPROVED" | "REJECTED";

export interface ContentLogInterface {
  id?: string;
  brand_id: string;
  brand_code: string;
  brand_name: string;
  creator_id: string;
  content_data: ContentData | null;
  content_type: string;
  status: ContentStatus;
  agent_feedback?: string | null;
  audit_by?: string | null;
  prompt_origin?: string | null;
  parent_id?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface ContentData {
  generated_content: string | null;
  text: string | null;
  llm_opinion: string | null;
  is_aligned: boolean | null;
}

export interface ContentLogUpdateInputsInterface {
  status: ContentStatus;
  agent_feedback?: string | null;
  audit_by?: string | null;
}

export interface ContentLogTableData {
  id?: string;
  brand_id: string;
  brand_code: string;
  brand_name: string;
  creator_id: string;
  content_data: ContentData;
  content_type: string;
  status: ContentStatus;
  agent_feedback?: string | null;
  audit_by?: string | null;
  prompt_origin?: string | null;
  created_at?: string;
  parent_id?: string | null;
}

export interface AuditPromptResponse {
  is_allowed: boolean;
  is_type_match: boolean;
  detected_content_type:
    | "PRODUCT_DESC"
    | "VIDEO_SCRIPT"
    | "IMAGE_PROMPT"
    | "SOCIAL_POST"
    | string;
  severity: "LOW" | "HIGH";
  feedback: string[];
  improved_prompt: string;
}
