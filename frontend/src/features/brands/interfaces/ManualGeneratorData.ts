

import type { GenerateManualInputs } from "../schemas/generarManual";


export interface AuditManualResponse {
  is_coherent: boolean;
  severity: 'LOW' | 'HIGH';
  feedback: string[];
  suggestions: string;
}


export interface ManualRecord {
  id?: string;
  brand_id: string;
  version: number;
  full_manual: string;
  raw_parameters: GenerateManualInputs;
  is_current_version: boolean;
  url_manual?: string;
  agent_feedback?: AuditManualResponse;
  created_at?: string; 
  updated_at?: string;
}

export interface RefineManualResponse {
  url_manual: string;
}