// src/common/components/ConfirmActionModal.tsx
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
} from "@mui/material";
import { IconAlertTriangle } from "@tabler/icons-react";

interface ConfirmActionModalProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  description: string;
  loading?: boolean;
}

export const ConfirmActionModal = ({
  open,
  onClose,
  onConfirm,
  title,
  description,
  loading,
}: ConfirmActionModalProps) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1,
          pt: 3,
          flexDirection: "column",
        }}
      >
        <IconAlertTriangle color="#d32f2f" size={50} />
        <Typography variant="h5" fontWeight="bold">
          {title}
        </Typography>
      </DialogTitle>

      <DialogContent sx={{ textAlign: "center" }}>
        <Typography variant="body1" color="text.secondary">
          {description}
        </Typography>
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
          onClick={onClose}
          variant="outlined"
          color="inherit"
          disabled={loading}
          sx={{ textTransform: "none", minWidth: "100px" }}
        >
          Cancelar
        </Button>
        <Button
          onClick={onConfirm}
          variant="contained"
          color="error"
          disabled={loading}
          sx={{
            textTransform: "none",
            minWidth: "100px",
          }}
        >
          {loading ? "..." : "Confirmar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
