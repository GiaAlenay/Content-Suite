import {
  TableCell,
  TableBody,
  TableRow,
  Tooltip,
  IconButton,
} from "@mui/material";
import React from "react";
import type { ContentLogTableData } from "../../interfaces/ContentLogData";
import type { Order } from "../../../../common/interfaces/common";
import {
  IconBulbFilled,
  IconEye,
  IconPencil,
  IconPencilBolt,
  IconPencilFilled,
  IconTrashFilled,
} from "@tabler/icons-react";

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
  contentLogList: ContentLogTableData[];
  order: Order;
  orderBy: keyof ContentLogTableData | string;
  page: number;
  rowsPerPage: number;
  onGenerateContenLog: (contentLog: ContentLogTableData) => void;
  onWatchContentLog: (contentLog: ContentLogTableData) => void;
}

const MyTableBody: React.FC<Props> = ({
  contentLogList,
  order,
  orderBy,
  page,
  rowsPerPage,
  onGenerateContenLog,
  onWatchContentLog,
}) => {
  const emptyRows =
    page > 0
      ? Math.max(0, (1 + page) * rowsPerPage - contentLogList.length)
      : 0;

  const visibleRows = React.useMemo(
    () =>
      contentLogList
        .sort(getComparator(order, orderBy))
        .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    [order, orderBy, page, rowsPerPage, contentLogList],
  );

  const renderTag = (status: string) => {
    if (status === "PENDING")
      return <div className="tag-item-estado tag-pending">Pendiente</div>;
    if (status === "APPROVED")
      return <div className="tag-item-estado tag-approved">Aprovado</div>;
    return <div className="tag-item-estado tag-rejected">Rechazado</div>;
  };

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
              }}
            >
              {row.brand_code}
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              {row.brand_name}
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              {row.created_at}
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              {row.content_type}
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              {renderTag(row.status)}
            </TableCell>
            <TableCell
              className="table-td"
              sx={{
                borderBottom:
                  index === visibleRows.length - 1 ? "none" : undefined,
              }}
            >
              <Tooltip title="Generar Manual">
                <IconButton onClick={() => onGenerateContenLog(row)}>
                  <IconPencilFilled />
                </IconButton>
              </Tooltip>

              <Tooltip title="Ver más información">
                <IconButton onClick={() => onWatchContentLog(row)}>
                  <IconEye />
                </IconButton>
              </Tooltip>
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
