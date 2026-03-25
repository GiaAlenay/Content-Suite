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


