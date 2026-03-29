import type { TableColumn } from "../../../common/interfaces/common";

export const headCells: TableColumn[] = [
 
  {
    id: "brand_code",
    numeric: false,
    disablePadding: false,
    label: "Codigo Marca",
    enableOrder:true,
    maxwidth: "170px",
  },
  {
    id: "brand_name",
    numeric: false,
    disablePadding: false,
    label: "Nombre Marca",
    enableOrder:true,
    maxwidth: "170px",
  },

   {
    id: "created_at",
    numeric: false,
    disablePadding: false,
    label: "Fecha Creación",
    enableOrder:true,
    maxwidth: "126px",
  },
  
  {
    id: "content_type",
    numeric: false,
    disablePadding: false,
    label: "Tipo de Contenido",
    enableOrder:true,
    maxwidth: "126px",
  },
 

  {
    id: "status",
    numeric: false,
    disablePadding: false,
    label: "Estado",
    enableOrder:true,
    maxwidth: "156px",
  },

   {
    id: "action",
    numeric: false,
    disablePadding: false,
    label: "Acciones",
    enableOrder:false,
    maxwidth: "156px",
  },
];


export const headCellsAdmin: TableColumn[] =[...headCells,
  {
  
    id: "creator_id",
    numeric: false,
    disablePadding: false,
    label: "Creador",
    enableOrder:true,
    maxwidth: "170px",
  
}]