import type { TableColumn } from "../../../../common/interfaces/common";

export const headCells: TableColumn[] = [
  {
    id: "logo_url",
    numeric: false,
    disablePadding: false,
    label: "Logo",
    enableOrder:false,
    maxwidth: "126px",
  },
  
  {
    id: "code",
    numeric: false,
    disablePadding: false,
    label: "Codigo Marca",
    enableOrder:true,
    maxwidth: "170px",
  },
  {
    id: "name",
    numeric: false,
    disablePadding: false,
    label: "Nombre Marca",
    enableOrder:true,
    maxwidth: "170px",
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