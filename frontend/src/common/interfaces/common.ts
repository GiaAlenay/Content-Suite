import type { User, Session } from '@supabase/supabase-js';
import type { LoginFormInputs } from '../utils/schemas';

export type Order = "asc" | "desc";
export interface TableColumn {
  id: string;         
  label: string;       
  numeric: boolean;    
  disablePadding: boolean;
  enableOrder:boolean;
  maxwidth?: string;  
}



export interface ApiResponseSuccess<T> {
  success: boolean;
  message: string;
  data: T;
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

export interface ListaSelectInterface{
  name:string;
  value:string
}