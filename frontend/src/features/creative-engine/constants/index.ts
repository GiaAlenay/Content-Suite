import type { ListaSelectInterface } from "../../../common/interfaces/common";

export const listaStatusDisponibles:ListaSelectInterface[]=[
  {
        name:"Creado",value:"CREATED"
    },
    {
        name:"Pendiente",value:"PENDING"
    },
     {
        name:"Aprovado",value:"APPROVED"
    },
     {
        name:"Rechazado",value:"REJECTED"
    }
]




export type ContentCategory = 'Ecommerce' | 'Social Media' | 'Video' | 'Email';

export interface ContentTypeOption {
  value: string;
  label: string;
  category: ContentCategory;
}

export const CONTENT_TYPE_OPTIONS: ContentTypeOption[] = [
  // Ecommerce
  { value: 'PRODUCT_DESC_LONG', label: 'Descripción Larga de Producto', category: 'Ecommerce' },
  { value: 'PRODUCT_BENEFITS', label: 'Lista de Beneficios', category: 'Ecommerce' },
  
  // Social Media
  { value: 'INSTAGRAM_POST', label: 'Post de Instagram', category: 'Social Media' },
  { value: 'TIKTOK_SCRIPT', label: 'Guion de TikTok (Vertical)', category: 'Social Media' },
  { value: 'LINKEDIN_POST', label: 'Post Corporativo (LinkedIn)', category: 'Social Media' },

  // Video
  { value: 'VIDEO_SCRIPT_ADS', label: 'Guion para Anuncio (Video)', category: 'Video' },
  
  // Email
  { value: 'EMAIL_PROMO', label: 'Email Promocional', category: 'Email' },
];

export const auditarRequestTitle="Solicitar auditoria"

export const auditarRequestQuestion= `¿Estás seguro de que deseas solicitar una auditoria para este contenido?.`