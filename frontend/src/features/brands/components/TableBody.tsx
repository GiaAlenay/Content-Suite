import { TableCell, TableBody, TableRow, Avatar, Chip } from "@mui/material";
import React from "react";
import type { BrandTableData } from "../interfaces/BrandData";
import type { Order } from "../../../common/interfaces/common";
function descendingComparator<T>(a: T, b: T, orderBy: keyof T) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order: Order, orderBy: string): (a, b) => number {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

interface Props {
  brandList: BrandTableData[];
  order: Order;
  orderBy: keyof BrandTableData | string;
  page: number;
  rowsPerPage: number;
}

const MyTableBody: React.FC<Props> = ({
  brandList,
  order,
  orderBy,
  page,
  rowsPerPage,
}) => {
  const emptyRows =
    page > 0 ? Math.max(0, (1 + page) * rowsPerPage - brandList.length) : 0;

  const visibleRows = React.useMemo(
    () =>
      brandList
        .sort(getComparator(order, orderBy))
        .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    [order, orderBy, page, rowsPerPage, brandList],
  );

  return (
    <TableBody>
      {visibleRows.map((row, index) => {
        return (
          <TableRow
            tabIndex={-1}
            key={row.id}
            sx={{
              borderBottom:
                index === visibleRows.length - 1 ? "none" : undefined,
              boxShadow: index === visibleRows.length - 1 && "none",
            }}
          >
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
                boxShadow: index === visibleRows.length - 1 && "none",
              }}
            >
              <Avatar
                src={row.logo_url}
                variant="rounded"
                sx={{ width: 40, height: 40 }}
              />
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              {row.code}
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              {row.name}
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              <Chip
                label={row.status}
                color={row.status === "ACTIVE" ? "success" : "default"}
                size="small"
                variant="outlined"
              />
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              actions
            </TableCell>
          </TableRow>
        );
      })}
      {emptyRows > 0 && (
        <TableRow
          style={{
            height: 53 * emptyRows,
          }}
        >
          <TableCell colSpan={6} />
        </TableRow>
      )}
    </TableBody>
  );
};
export default MyTableBody;
