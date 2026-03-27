import {
  TableCell,
  TableHead,
  TableRow,
  TableSortLabel,
  Box,
} from "@mui/material";

import { visuallyHidden } from "@mui/utils";
import type { Order, TableColumn } from "../../../../common/interfaces/common";
import type { BrandTableData } from "../../interfaces/BrandData";
import { headCells } from "./headCell";

function MyTableHead({
  order,
  orderBy,
  onRequestSort,
}: {
  order: Order;
  orderBy: keyof BrandTableData | string;
  onRequestSort: (property: string) => void;
}) {
  const createSortHandler = (property: string) => () => {
    onRequestSort(property);
  };

  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell: TableColumn) => (
          <TableCell
            className="table-title"
            key={headCell.id}
            align={"left"}
            padding={headCell.disablePadding ? "none" : "normal"}
            sortDirection={orderBy === headCell.id ? order : false}
            style={{
              padding: "10px",
              maxWidth: `${headCell.maxwidth ?? "auto"}`,
              fontWeight: "600 !important",
            }}
          >
            {headCell.enableOrder ? (
              <TableSortLabel
                active={orderBy === headCell.id}
                direction={orderBy === headCell.id ? order : "asc"}
                onClick={createSortHandler(headCell.id)}
              >
                {headCell.label}
                {orderBy === headCell.id ? (
                  <Box component="span" sx={visuallyHidden}>
                    {order === "desc"
                      ? "sorted descending"
                      : "sorted ascending"}
                  </Box>
                ) : null}
              </TableSortLabel>
            ) : (
              headCell.label
            )}
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

export default MyTableHead;
