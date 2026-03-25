import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Box,
  TableFooter,
} from "@mui/material";
import { visuallyHidden } from "@mui/utils";
import { useEffect, useState } from "react";
import AgregarAnticipo from "./agregarAnticipo";
import { Pencil } from "tabler-icons-react";
import AgregarMontoSAF from "./agregarMontoSAF";
import { SkeletonOption } from "../../../components/ui/shared/skeleton";

const headCells = [
  {
    id: "numeroFile",
    numeric: false,
    disablePadding: false,
    label: "Nro. de File",
    maxwidth: "126px",
  },

  {
    id: "numeroPI",
    numeric: false,
    disablePadding: false,
    label: "Nro. de PI",
    maxwidth: "170px",
  },
  {
    id: "descripcion",
    numeric: false,
    disablePadding: false,
    label: "Descripción",
    maxwidth: "170px",
  },
  {
    id: "fechaOperacionFile",
    numeric: false,
    disablePadding: false,
    label: "Fecha de Operación",
    maxwidth: "176px",
  },

  {
    id: "total",
    numeric: true,
    disablePadding: false,
    label: "Valor Nominal",
    maxwidth: "156px",
  },

  {
    id: "totalPagado",
    numeric: true,
    disablePadding: false,
    label: "Monto Cobrado",
    maxwidth: "156px",
  },

  {
    id: "pendienteCobrar",
    numeric: true,
    disablePadding: false,
    label: "Pendiente a Cobrar",
    maxwidth: "156px",
  },
  {
    id: "cobradoSAF",
    numeric: true,
    disablePadding: false,
    label: "Cobrado con SAF",
    maxwidth: "156px",
  },
  {
    id: "montoCobrar",
    numeric: true,
    disablePadding: false,
    label: "Monto a Cobrar",
    maxwidth: "156px",
  },
];

interface Props {
  account: any;
  dataPagosPendientes: any[];
  setresultPagosPendientes: any;
  setresultPagosPendientesCopy: any;
  error: any;
  isLoadingPagosPendientes: boolean;
}
type Order = "asc" | "desc";
const TablePagosPendientes: React.FC<Props> = ({
  account,
  dataPagosPendientes,
  setresultPagosPendientes,
  setresultPagosPendientesCopy,
  isLoadingPagosPendientes,
  error,
}) => {
  const [order, setOrder] = useState<Order>("asc");
  const [orderBy, setOrderBy] = useState<string>("numeroFile");

  const [total, setTotal] = useState<number>(0);
  const [totalPagado, setTotalPagado] = useState<number>(0);
  const [pendienteCobrar, setPendienteCobrar] = useState<number>(0);
  const [cobradoSAF, setCobradoSAF] = useState<number>(0);
  const [montoCobrar, setMontoCobrar] = useState<number>(0);

  const [openDialogAnticipo, setOpenDialogAnticipo] = useState<boolean>(false);
  const [openDialogSAF, setOpenDialogSAF] = useState<boolean>(false);
  const [rowSelected, setRowSelected] = useState<any>(null);
  let content;

  useEffect(() => {
    if (dataPagosPendientes.length === 0) return;

    const totals = dataPagosPendientes.reduce(
      (acc, p) => {
        acc.total += Number(p.total) || 0;
        acc.totalPagado += Number(p.totalPagado) || 0;
        acc.pendienteCobrar += Number(p.pendienteCobrar) || 0;
        acc.cobradoSAF += Number(p.cobradoSAF) || 0;
        acc.montoCobrar += Number(p.montoCobrar) || 0;
        return acc;
      },
      {
        total: 0,
        totalPagado: 0,
        pendienteCobrar: 0,
        cobradoSAF: 0,
        montoCobrar: 0,
      },
    );

    setTotal(parseFloat(totals.total.toFixed(2)));
    setTotalPagado(parseFloat(totals.totalPagado.toFixed(2)));
    setPendienteCobrar(parseFloat(totals.pendienteCobrar.toFixed(2)));
    setCobradoSAF(parseFloat(totals.cobradoSAF.toFixed(2)));
    setMontoCobrar(parseFloat(totals.montoCobrar.toFixed(2)));
  }, [dataPagosPendientes]);

  const handleRequestSort = (
    event: React.MouseEvent<unknown>,
    property: string,
  ) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  if (isLoadingPagosPendientes) {
    content = <SkeletonOption />;
  } else if (dataPagosPendientes.length === 0 && !error) {
    content = (
      <div className="errorCont emptyTable">
        Lo sentimos. No tenemos pagos pendientes con este numero de File. Por
        favor, intenta con otro valor.
      </div>
    );
  } else if (dataPagosPendientes.length > 0) {
    content = (
      <TableContainer sx={{ maxHeight: 477 }}>
        <Table stickyHeader aria-label="sticky table">
          <MyTableHead
            order={order}
            orderBy={orderBy}
            onRequestSort={handleRequestSort}
            rowCount={dataPagosPendientes.length}
          />
          <TableBody>
            {dataPagosPendientes.map((row, index) => (
              <TableRow key={index}>
                <TableCell className="table-td">{row.numeroFile}</TableCell>
                <TableCell className="table-td">{row.numeroPI}</TableCell>
                <TableCell className="table-td">{row.descripcion}</TableCell>
                <TableCell className="table-td">
                  {row.fechaOperacionFile}
                </TableCell>
                <TableCell className="table-td">{row.total}</TableCell>
                <TableCell className="table-td">{row.totalPagado}</TableCell>
                <TableCell className="table-td">
                  {row.pendienteCobrar}
                </TableCell>
                <TableCell className="table-td">
                  <div
                    className="row-base"
                    style={{
                      width: "80%",
                      gap: "5px",
                      justifyContent: "space-between",
                    }}
                  >
                    <span>{row.cobradoSAF}</span>
                    {row.tipo !== "anticipo" && row.pendienteCobrar !== 0 && (
                      <Pencil
                        size={20}
                        onClick={() => {
                          setRowSelected(row);
                          setOpenDialogSAF(true);
                        }}
                      />
                    )}
                  </div>
                </TableCell>
                <TableCell className="table-td">{row.montoCobrar}</TableCell>
              </TableRow>
            ))}
          </TableBody>

          <TableFooter>
            <TableRow
              sx={{
                position: "sticky",
                bottom: 0,
                backgroundColor: "#ffffff",
                fontWeight: "bold",
                borderBottom: "none",
                boxShadow: "none",
              }}
            >
              <TableCell
                className="table-td-total"
                style={{ color: "red !important" }}
                sx={{ borderBottom: "none" }}
              >
                Total
              </TableCell>
              <TableCell
                className="table-td-total"
                sx={{ borderBottom: "none" }}
              ></TableCell>
              <TableCell
                className="table-td-total"
                sx={{ borderBottom: "none" }}
              ></TableCell>
              <TableCell
                className="table-td-total"
                sx={{ borderBottom: "none" }}
              ></TableCell>
              <TableCell
                className="table-td-total"
                sx={{ borderBottom: "none" }}
              >
                ${total}
              </TableCell>
              <TableCell
                className="table-td-total"
                sx={{ borderBottom: "none" }}
              >
                $ {totalPagado}
              </TableCell>
              <TableCell
                className="table-td-total"
                sx={{ borderBottom: "none" }}
              >
                ${pendienteCobrar}
              </TableCell>
              <TableCell
                className="table-td-total"
                sx={{ borderBottom: "none" }}
              >
                ${cobradoSAF}
              </TableCell>
              <TableCell
                className="table-td-total"
                sx={{ borderBottom: "none" }}
              >
                $ {montoCobrar}
              </TableCell>
            </TableRow>
          </TableFooter>
        </Table>
      </TableContainer>
    );
  } else if (error) {
    content = <div className="errorCont emptyTable">{error}</div>;
  }

  return (
    <div className="table-Title-cont">
      <div
        className="row-base "
        style={{ justifyContent: "space-between", gap: "30px" }}
      >
        <h4 className="tableTitle">Ver Pagos Pendientes</h4>
        <button
          className="btn-base btn-full-orange "
          onClick={() => {
            setOpenDialogAnticipo(true);
          }}
        >
          Agregar Anticipo
        </button>

        <AgregarAnticipo
          account={account}
          open={openDialogAnticipo}
          setOpen={setOpenDialogAnticipo}
          setresultPagosPendientes={setresultPagosPendientes}
          setresultPagosPendientesCopy={setresultPagosPendientesCopy}
        />
      </div>

      {content}
      {openDialogSAF && (
        <AgregarMontoSAF
          invoice={{ ...rowSelected, period: account.period }}
          open={openDialogSAF}
          setOpen={setOpenDialogSAF}
          setresultPagosPendientes={setresultPagosPendientes}
          setresultPagosPendientesCopy={setresultPagosPendientesCopy}
        />
      )}
    </div>
  );
};
export default TablePagosPendientes;

function MyTableHead(props) {
  const { order, orderBy, rowCount, onRequestSort } = props;
  const createSortHandler =
    (property) => (event: React.MouseEvent<unknown>) => {
      onRequestSort(event, property);
    };

  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell) => (
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
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

/////////////////////////////////////////////////////////////////////////

import React, { useState } from "react";
import Box from "@mui/material/Box";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import TableSortLabel from "@mui/material/TableSortLabel";
import Paper from "@mui/material/Paper";
import { visuallyHidden } from "@mui/utils";
import { SkeletonOption } from "../../../components/ui/shared/skeleton";

interface Data {
  id: string;
  numeroFile: string;
  notaCredito: string;
  descripcion: string;
  monto: string;
  incremento: string;
}
interface Props {
  dataIncrementos: any[];
  error: any;
  isLoadingIncrementos: boolean;
}

const TableIncremento: React.FC<Props> = ({
  dataIncrementos,
  error,
  isLoadingIncrementos,
}) => {
  const [order, setOrder] = useState<Order>("asc");
  const [orderBy, setOrderBy] = useState<keyof Data>("numeroFile");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  let content;
  const handleRequestSort = (
    event: React.MouseEvent<unknown>,
    property: keyof Data,
  ) => {
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

  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows =
    page > 0
      ? Math.max(0, (1 + page) * rowsPerPage - dataIncrementos.length)
      : 0;

  const visibleRows = React.useMemo(
    () =>
      dataIncrementos
        .sort(getComparator(order, orderBy))
        .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    [order, orderBy, page, rowsPerPage, dataIncrementos],
  );

  if (isLoadingIncrementos) {
    content = <SkeletonOption />;
  } else if (dataIncrementos.length === 0 && !error) {
    content = (
      <div className="errorCont emptyTable">
        Lo sentimos. No tenemos incrementos con este numero de File. Por favor,
        intenta con otro valor.
      </div>
    );
  } else if (dataIncrementos.length > 0) {
    content = (
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
          <TableContainer>
            <Table
              sx={{ minWidth: 750 }}
              aria-labelledby="tableTitle"
              size="medium"
            >
              <MyTableHead
                order={order}
                orderBy={orderBy}
                onRequestSort={handleRequestSort}
                rowCount={dataIncrementos.length}
              />
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
                            index === visibleRows.length - 1
                              ? "none"
                              : undefined,
                          boxShadow: index === visibleRows.length - 1 && "none",
                        }}
                      >
                        {row.numeroFile}
                      </TableCell>
                      <TableCell
                        className="table-td"
                        sx={{
                          borderBottom:
                            index === visibleRows.length - 1
                              ? "none"
                              : undefined,
                        }}
                      >
                        {row.notaCredito}
                      </TableCell>
                      <TableCell
                        className="table-td"
                        sx={{
                          borderBottom:
                            index === visibleRows.length - 1
                              ? "none"
                              : undefined,
                        }}
                      >
                        {row.descripcion}
                      </TableCell>
                      <TableCell
                        className="table-td"
                        sx={{
                          borderBottom:
                            index === visibleRows.length - 1
                              ? "none"
                              : undefined,
                        }}
                      >
                        {row.tipo !== "NC" && "-"}
                        {row.monto}
                      </TableCell>
                      <TableCell
                        className="table-td"
                        sx={{
                          borderBottom:
                            index === visibleRows.length - 1
                              ? "none"
                              : undefined,
                        }}
                      >
                        {row.incremento}
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
            </Table>
          </TableContainer>
          <TablePagination
            style={{ fontSize: "12px", width: "100%" }}
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={dataIncrementos.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      </Box>
    );
  } else if (error) {
    content = <div className="errorCont emptyTable">{error}</div>;
  }
  return (
    <div className="table-Title-cont">
      <h4 className="tableTitle">Ver Incrementos</h4>
      {content}
    </div>
  );
};
export default TableIncremento;

function descendingComparator<T>(a: T, b: T, orderBy: keyof T) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

type Order = "asc" | "desc";

function getComparator(order: Order, orderBy: string): (a, b) => number {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

interface HeadCell {
  disablePadding: boolean;
  id: keyof Data;
  label: string;
  numeric: boolean;
  maxwidth?: string;
}

const headCells: readonly HeadCell[] = [
  {
    id: "numeroFile",
    numeric: false,
    disablePadding: false,
    label: "Nro. de File",
    maxwidth: "110px",
  },
  {
    id: "notaCredito",
    numeric: false,
    disablePadding: false,
    label: "Nota de Crédito",
  },
  {
    id: "descripcion",
    numeric: false,
    disablePadding: false,
    label: "Descripción",
    maxwidth: "120px",
  },
  {
    id: "monto",
    numeric: true,
    disablePadding: false,
    label: "Monto",
    maxwidth: "75px",
  },

  {
    id: "incremento",
    numeric: true,
    disablePadding: false,
    label: "Incremento",
  },
];

interface MyTableHeadProps {
  onRequestSort: (
    event: React.MouseEvent<unknown>,
    property: keyof Data,
  ) => void;
  order: Order;
  orderBy: string;
  rowCount: number;
}

function MyTableHead(props: MyTableHeadProps) {
  const { order, orderBy, rowCount, onRequestSort } = props;
  const createSortHandler =
    (property: keyof Data) => (event: React.MouseEvent<unknown>) => {
      onRequestSort(event, property);
    };

  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={"left"}
            padding={headCell.disablePadding ? "none" : "normal"}
            sortDirection={orderBy === headCell.id ? order : false}
            className="table-title"
            style={{
              padding: "10px",
              maxWidth: `${headCell.maxwidth ?? "auto"}`,
              fontWeight: "600 !important",
            }}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}
