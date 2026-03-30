import {
  Table,
  TableContainer,
  Paper,
  Box,
  TablePagination,
} from "@mui/material";
import MyTableHead from "./TableHead";
import MyTableBody from "./TableBody";
import { useState } from "react";
import type { ContentLogTableData } from "../../interfaces/ContentLogData";
import type { Order } from "../../../../common/interfaces/common";

export const ContentLogTable = ({
  data,
  onUpdateStatusContenLog,
  onWatchContentLog,
}: {
  data: ContentLogTableData[];
  onUpdateStatusContenLog: (contentLog: ContentLogTableData) => void;
  onWatchContentLog: (contentLog: ContentLogTableData) => void;
}) => {
  const [order, setOrder] = useState<Order>("asc");
  const [orderBy, setOrderBy] = useState<keyof ContentLogTableData | string>(
    "code",
  );
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const handleRequestSort = (property: string) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <Box sx={{ width: "100%" }}>
      <Paper
        sx={{
          width: "100%",
          boxShadow: "none",
          display: "flex",
          flexDirection: "column",
          gap: "30px",
        }}
      >
        <TableContainer sx={{ maxHeight: 477 }}>
          <Table>
            <MyTableHead
              order={order}
              orderBy={orderBy}
              onRequestSort={handleRequestSort}
            />
            <MyTableBody
              contentLogList={data}
              order={order}
              orderBy={orderBy}
              page={page}
              rowsPerPage={rowsPerPage}
              onUpdateStatusContenLog={onUpdateStatusContenLog}
              onWatchContentLog={onWatchContentLog}
            />
          </Table>
        </TableContainer>
        <TablePagination
          style={{ fontSize: "12px", width: "100%" }}
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={data.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </Box>
  );
};
