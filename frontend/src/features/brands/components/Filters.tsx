import React,  from 'react';
import InputAdornment from '@material-ui/core/InputAdornment';
import TextField from '@material-ui/core/TextField';
import SearchIcon from '@material-ui/icons/Search';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';

interface Props {
  codigo: string;
  setCodigo: React.Dispatch<React.SetStateAction<string>>;
  searchValue: string;
  setSearchValue: React.Dispatch<React.SetStateAction<string>>;
  listaCodigosDisponibles: string[];
}
const Filtros: React.FC<Props> = ({
  codigo,
  setCodigo,
  searchValue,
  setSearchValue,
  listaCodigosDisponibles,
}) => {
  const handleChangeCodigo = (event: SelectChangeEvent) => {
    setCodigo(event.target.value);
  };

  const handleChangeSearchValue = (e) => {
    setSearchValue(e.target.value);
  };

  return (
    <div className="filtros-dialog-cont">
      <div className="form-field-cont hijo">
        <div className="field-name">Buscador</div>
        <TextField
          style={{ minWidth: '220px' }}
          placeholder="Buscar..."
          type="text"
          variant="outlined"
          fullWidth
          onChange={handleChangeSearchValue}
          value={searchValue}
          InputProps={{
            classes: {
              root: 'custom-outlined-input-root',
              focused: 'custom-outlined-input-focused',
            },
            endAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
      </div>

      <div className="form-field-cont hijo">
        {' '}
        <div className="field-name">Código</div>{' '}
        <Select
          value={codigo}
          onChange={handleChangeCodigo}
          displayEmpty
          inputProps={{ 'aria-label': 'Without label' }}
          style={{
            minWidth: '220px',
            maxHeight: '56px',
            height: '56px',
            textAlign: 'left',
          }}
        >
          <MenuItem value="">
            <em>Todos</em>
          </MenuItem>
          {listaCodigosDisponibles.map((e: string, i: number) => (
            <MenuItem key={i} value={e} style={{ color: '#2A3547' }}>
              {e}
            </MenuItem>
          ))}
        </Select>
      </div>
    </div>
  );
};

export default Filtros;


import React, { useEffect, useState } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { CircularProgress } from '@mui/material';
import NotificationService from '../../../utils/toaster';
import { TextField, InputAdornment } from '@mui/material';
import { Moneybag, Menu2 } from 'tabler-icons-react';
import { UpdateInvoiceFunction } from '../queryFunctions/UpdateInvoice';
interface Props {
  invoice: any;
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setresultPagosPendientes: any;
  setresultPagosPendientesCopy: any;
}

const AgregarMontoSAF: React.FC<Props> = ({
  invoice,
  open,
  setOpen,
  setresultPagosPendientes,
  setresultPagosPendientesCopy,
}) => {
  const [myFormValues, setMyFormValues] = useState<any>({ monto: null });
  const [confirmUpdate, setConfirmUpdate] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingUpdate, isSuccessUpdate, MsgUpdate] = UpdateInvoiceFunction(
    invoice,
    myFormValues.monto,
    confirmUpdate
  );
  const handleVincular = () => {
    setConfirmUpdate(true);
  };

  useEffect(() => {
    if (confirmUpdate && isSuccessUpdate !== null && MsgUpdate !== null) {
      setOpen(false);
      setConfirmUpdate(false);

      if (isSuccessUpdate) {
        NotificationService.showSuccessAlert(String(MsgUpdate));
        updateLocalListaAnticipoes();
      } else {
        NotificationService.notifyError(String(MsgUpdate));
        setConfirmUpdate(false);
      }
    }
  }, [confirmUpdate, isSuccessUpdate, MsgUpdate]);

  const updateLocalListaAnticipoes = () => {
    setresultPagosPendientes((prev: any) => {
      const findInvoice = prev.find((t: any) => t.id === invoice.id);

      if (findInvoice) {
        findInvoice.cobradoSAF = Number(myFormValues.monto);
        findInvoice.montoCobrar =
          findInvoice.total - findInvoice.totalPagado - findInvoice.cobradoSAF;
      }
      return [...prev];
    });
    setresultPagosPendientesCopy((prev: any) => {
      const findInvoice = prev.find((t: any) => t.id === invoice.id);
      if (findInvoice) {
        findInvoice.cobradoSAF = Number(myFormValues.monto);
        findInvoice.montoCobrar =
          findInvoice.total - findInvoice.totalPagado - findInvoice.cobradoSAF;
      }
      return [...prev];
    });
  };

  const onNumberInput = (value: string) => {
    const cleanValue = value
      .replace(/[^0-9.]/g, '')
      .replace(/(\..*?)\..*/g, '$1');
    if (cleanValue && parseFloat(cleanValue) > invoice?.pendienteCobrar) {
      setError(`El monto no puede ser mayor a ${invoice?.pendienteCobrar}`);
    } else {
      setError(null);
    }
    return cleanValue;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = onNumberInput(e.target.value);
    setMyFormValues((prev: any) => ({
      ...prev,
      monto: newValue,
    }));
  };

  const handleClose = () => {
    setMyFormValues({ monto: null });
    setOpen(false);
  };

  return (
    <Dialog
      fullWidth={true}
      open={open}
      onClose={handleClose}
      sx={{
        '& .MuiDialog-paper': {
          maxWidth: '410px',
          gap: '30px',
          padding: '30px',
          minHeight: 'fit-content',
        },
      }}
    >
      <DialogTitle style={{ padding: '0' }} className="dialog-title row-base">
        <h5>Añadir Monto SAF a Cobrar </h5>
      </DialogTitle>
      <DialogContent style={{ padding: '0' }}>
        <div className="balance-completo column-base " style={{ gap: '30px' }}>
          <div
            className="invoice-details-cont column-base"
            style={{ gap: '10px' }}
          >
            <div className="invoice-detail row-base" style={{ gap: '20px' }}>
              <span className="sub">Nro. de File:</span>
              <span>{invoice.numeroFile}</span>
            </div>
            <div className="invoice-detail row-base" style={{ gap: '20px' }}>
              <span className="sub">Nro. de PI:</span>
              <span>{invoice.numeroPI}</span>
            </div>
            <div className="invoice-detail row-base" style={{ gap: '20px' }}>
              <span className="sub">Pendiente a Cobrar:</span>
              <span>$ {invoice.pendienteCobrar}</span>
            </div>
            <div className="invoice-detail row-base" style={{ gap: '20px' }}>
              <span className="sub">SAF Disponible:</span>
              <span>$ {invoice.cobradoSAF}</span>
            </div>
          </div>
          <div className="row-base vertical-center" style={{ gap: '8px' }}>
            <span className="field-name">Monto SAF</span>
            <TextField
              value={myFormValues.monto || ''}
              onChange={handleChange}
              variant="outlined"
              placeholder="Añade un monto"
              fullWidth
              error={!!error}
              helperText={error}
              sx={{
                maxHeight: '48px',
                '& .MuiOutlinedInput-root': {
                  height: '48px',
                  '& input': {
                    padding: '10px 14px',
                  },
                },
              }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Moneybag color="#808080" />
                  </InputAdornment>
                ),
              }}
            />
          </div>
        </div>
      </DialogContent>
      <DialogActions
        style={{ padding: '0', justifyContent: 'center', gap: '30px' }}
      >
        <button
          className="btn-base btn-full-orange "
          style={{ width: '160px' }}
          disabled={
            !myFormValues.monto ||
            parseFloat(myFormValues.monto) > invoice?.pendienteCobrar
              ? true
              : false
          }
          onClick={handleVincular}
        >
          {loadingUpdate ? (
            <div className="loadingBtn">
              Agregando
              <CircularProgress size={20} style={{ color: '#FFFFFF' }} />
            </div>
          ) : (
            <>Agregar Monto</>
          )}
        </button>
        <button
          style={{ width: '160px' }}
          className="btn-base btn-lines-orange "
          onClick={() => {
            setOpen(false);
          }}
        >
          Cancelar
        </button>
      </DialogActions>
    </Dialog>
  );
};
export default AgregarMontoSAF;