import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  Grid,
  IconButton,
  CircularProgress,
} from "@mui/material";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { UploadFile } from "../../../../common/components/StorageService/UploadFile";
import {
  CreateBrandSchema,
  type CreateBrandInputs,
} from "../../schemas/agregarBrand";
import { IconX } from "@tabler/icons-react";

interface AddBrandModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (data: CreateBrandInputs, onSuccess: () => void) => void;
  isLoading: boolean;
  setFile: (file: File) => void;
}

export const AddBrandModal = ({
  open,
  onClose,
  onSave,
  isLoading,
  setFile,
}: AddBrandModalProps) => {
  const {
    control,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CreateBrandInputs>({
    resolver: zodResolver(CreateBrandSchema),
    defaultValues: { code: "", name: "", description: "" },
  });

  const handleFullOnClose = () => {
    reset();
    onClose();
  };

  const handleFormSubmit = (data: CreateBrandInputs) => {
    if (isLoading) return;
    onSave(data, reset);
  };

  return (
    <Dialog open={open} onClose={handleFullOnClose} fullWidth maxWidth="xs">
      <DialogTitle
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
          fontWeight: "bold",
        }}
      >
        <Typography variant="h6" fontWeight="bold" component="span">
          Añadir Nueva Marca
        </Typography>
        <IconButton
          onClick={handleFullOnClose}
          sx={{ ml: "auto" }}
          size="small"
        >
          <IconX size={20} />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        <Box component="form" sx={{ mt: 2.5 }}>
          <UploadFile setFile={(file: File) => setFile(file)} />

          {/* <Grid container spacing={2}> */}
          <Grid sx={{ mt: 2.5 }}>
            <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
              Código *
            </Typography>
            <Controller
              name="code"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  placeholder="QS-001"
                  error={!!errors.code}
                  helperText={errors.code?.message}
                />
              )}
            />
          </Grid>

          <Grid sx={{ mt: 2.5 }}>
            <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
              Nombre de Marca *
            </Typography>
            <Controller
              name="name"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  placeholder="Nombre de la marca"
                  error={!!errors.name}
                  helperText={errors.name?.message}
                />
              )}
            />
          </Grid>

          <Grid sx={{ mt: 2.5 }}>
            <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
              Descripción
            </Typography>
            <Controller
              name="description"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  multiline
                  rows={4}
                  placeholder="Breve descripción de la marca..."
                  sx={{
                    "& .MuiOutlinedInput-root": {
                      minHeight: "48px",
                      height: "auto",
                      p: "10px 14px",
                    },
                    "& .MuiOutlinedInput-input": { p: 0 },
                  }}
                />
              )}
            />
          </Grid>
          {/* </Grid> */}
        </Box>
      </DialogContent>

      <DialogActions
        sx={{
          p: 3,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 1.5,
        }}
      >
        <Button
          onClick={handleFullOnClose}
          color="inherit"
          variant="outlined"
          sx={{ textTransform: "none", minWidth: "100px" }}
        >
          Cancelar
        </Button>
        <Button
          onClick={handleSubmit(handleFormSubmit)}
          sx={{ textTransform: "none", minWidth: "100px" }}
          variant="contained"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="loadingBtn">
              <CircularProgress size={20} style={{ color: "#FFFFFF" }} />
            </div>
          ) : (
            <>Guardar</>
          )}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
