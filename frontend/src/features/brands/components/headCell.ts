import type { TableColumn } from "../../../common/interfaces/common";

export const headCells: TableColumn[] = [
  {
    id: "logo_url",
    numeric: false,
    disablePadding: false,
    label: "Logo",
    maxwidth: "126px",
  },
  
  {
    id: "code",
    numeric: false,
    disablePadding: false,
    label: "Codigo Marca",
    maxwidth: "170px",
  },
  {
    id: "name",
    numeric: false,
    disablePadding: false,
    label: "Nombre Marca",
    maxwidth: "170px",
  },
 

  {
    id: "status",
    numeric: false,
    disablePadding: false,
    label: "Estatus",
    maxwidth: "156px",
  },

   {
    id: "action",
    numeric: false,
    disablePadding: false,
    label: "Acciones",
    maxwidth: "156px",
  },
];