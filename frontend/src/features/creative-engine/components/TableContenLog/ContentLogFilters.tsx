import type { SelectChangeEvent } from "@mui/material";
import { TextField, MenuItem, InputAdornment, Select } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import type { ListaSelectInterface } from "../../../../common/interfaces/common";
interface Props {
  status: string;
  setStatus: React.Dispatch<React.SetStateAction<string>>;
  searchValue: string;
  setSearchValue: React.Dispatch<React.SetStateAction<string>>;
  listaStatusDisponibles: ListaSelectInterface[];
}
const ContentLogFilters: React.FC<Props> = ({
  status,
  setStatus,
  searchValue,
  setSearchValue,
  listaStatusDisponibles,
}) => {
  const handleChangeStatus = (event: SelectChangeEvent) => {
    setStatus(event.target.value);
  };

  const handleChangeSearchValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value);
  };

  return (
    <div className="filtros-dialog-cont" style={{ width: "100%" }}>
      <div className="form-field-cont hijo">
        <div className="field-name">Buscador</div>
        <TextField
          style={{ minWidth: "220px" }}
          placeholder="Buscar..."
          type="text"
          variant="outlined"
          fullWidth
          onChange={handleChangeSearchValue}
          value={searchValue}
          InputProps={{
            endAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
      </div>

      <div className="form-field-cont hijo">
        {" "}
        <div className="field-name">Estado</div>{" "}
        <Select
          value={status}
          onChange={handleChangeStatus}
          displayEmpty
          inputProps={{ "aria-label": "Without label" }}
          style={{
            minWidth: "220px",
            maxHeight: "48px",
            height: "48px",
            textAlign: "left",
          }}
        >
          <MenuItem value="">
            <em>Todos</em>
          </MenuItem>
          {listaStatusDisponibles.map((e: ListaSelectInterface, i: number) => (
            <MenuItem key={i} value={e.value} style={{ color: "#2A3547" }}>
              {e.name}
            </MenuItem>
          ))}
        </Select>
      </div>
    </div>
  );
};

export default ContentLogFilters;
