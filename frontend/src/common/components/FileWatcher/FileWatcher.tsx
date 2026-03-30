import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  IconButton,
  Box,
  CircularProgress,
  Typography,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import DownloadIcon from "@mui/icons-material/GetApp";

interface Props {
  open: boolean;
  onClose: () => void;
  pdfUrl: string | null;
  title?: string;
}

export const PDFViewerModal: React.FC<Props> = ({
  open,
  onClose,
  pdfUrl,
  title = "Visualizar PDF",
}) => {
  const [loading, setLoading] = useState(true);

  if (!pdfUrl) return null;

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: { height: "80vh" }, // Altura fija para que el iframe sea usable
      }}
    >
      <DialogTitle
        sx={{
          m: 0,
          p: 2,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="h6" component="div" sx={{ fontWeight: "bold" }}>
          {title}
        </Typography>

        <div>
          <IconButton onClick={onClose} href={pdfUrl} target="_blank" download>
            <DownloadIcon />
          </IconButton>
          <IconButton onClick={onClose} aria-label="close">
            <CloseIcon />
          </IconButton>
        </div>
      </DialogTitle>

      <DialogContent
        dividers
        sx={{ p: 0, position: "relative", overflow: "hidden" }}
      >
        {/* Loader mientras el PDF carga en el iframe */}
        {loading && (
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              gap: 2,
            }}
          >
            <CircularProgress />
            <Typography variant="body2" color="text.secondary">
              Cargando documento...
            </Typography>
          </Box>
        )}

        <iframe
          src={`${pdfUrl}#toolbar=0`}
          width="100%"
          height="100%"
          style={{
            border: "none",
            display: loading ? "none" : "block",
          }}
          onLoad={() => setLoading(false)}
          title="PDF Preview"
        />
      </DialogContent>

      <DialogActions
        sx={{ p: 2, justifyContent: "space-between" }}
      ></DialogActions>
    </Dialog>
  );
};
