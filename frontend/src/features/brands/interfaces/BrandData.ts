export interface BrandTableData {
  id: string;
  code: string;
  name: string;
  logo_url: string;
  status: string;
  description: string;
}


export interface BrandInterface {
  id: string ;
  name: string;
  code: string;
  description: string;
  logo_url: string;
  status: 'ACTIVE' | 'INACTIVE';
  created_at: string | null;
  updated_at: string | null;
}