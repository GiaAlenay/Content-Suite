import { TextField, InputAdornment } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
interface Props {
  searchValue: string;
  setSearchValue: React.Dispatch<React.SetStateAction<string>>;
}
const BrandFilters: React.FC<Props> = ({ searchValue, setSearchValue }) => {
  const handleChangeSearchValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value);
  };

  return (
    <div className="filtros-dialog-cont" style={{ width: "50%" }}>
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
    </div>
  );
};

export default BrandFilters;
