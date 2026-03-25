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
import type { BrandTableData } from "../interfaces/BrandData";
import type { Order } from "../../../common/interfaces/common";

export const BrandTable = ({ data }: { data: BrandTableData[] }) => {
  const [order, setOrder] = useState<Order>("asc");
  const [orderBy, setOrderBy] = useState<keyof BrandTableData | string>("code");
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
              brandList={data}
              order={order}
              orderBy={orderBy}
              page={page}
              rowsPerPage={rowsPerPage}
            />
            {/* <TableBody>
          {filteredData.map((brand: any) => (
            <TableRow key={brand.id} hover>
              <TableCell>
                <Avatar
                  src={brand.logo_url}
                  variant="rounded"
                  sx={{ width: 40, height: 40 }}
                />
              </TableCell>
              <TableCell>{brand.code}</TableCell>
              <TableCell>{brand.name}</TableCell>
              <TableCell>
                <Chip
                  label={brand.status}
                  color={brand.status === "ACTIVE" ? "success" : "default"}
                  size="small"
                  variant="outlined"
                />
              </TableCell>
              <TableCell align="right">
                <Stack direction="row" spacing={1} justifyContent="flex-end">
                  <Tooltip title="Generar Manual">
                    <IconButton color="primary" size="small">
                      <AutoFixHighIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Editar">
                    <IconButton size="small">
                      <EditIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Eliminar">
                    <IconButton color="error" size="small">
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </Stack>
              </TableCell>
            </TableRow>
          ))}
        </TableBody> */}
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
