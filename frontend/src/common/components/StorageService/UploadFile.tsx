import { Box, Button, Typography } from "@mui/material";
import { IconUpload, IconPhoto } from "@tabler/icons-react";
import { useState } from "react";

interface UploadFileProps {
  setFile: (file: File) => void;
  currentLogo?: string;
  isLoading?: boolean;
}

export const UploadFile = ({
  setFile,
  currentLogo,
  isLoading,
}: UploadFileProps) => {
  const [preview, setPreview] = useState(currentLogo || "");

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));

    setFile(file);
  };

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 3,
        mb: 3,
      }}
    >
      <Box
        sx={{
          width: 100,
          height: 100,
          borderRadius: 2,
          border: "2px dashed #ccc",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
          bgcolor: "#f9f9f9",
        }}
      >
        {preview ? (
          <img
            src={preview}
            alt="Logo Preview"
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <IconPhoto color="#ccc" size={32} />
        )}
      </Box>

      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Button
          variant="outlined"
          component="label"
          startIcon={<IconUpload size={20} />}
          disabled={isLoading}
          sx={{ textTransform: "none", width: "140px" }}
        >
          Subir
          <input
            type="file"
            hidden
            accept="image/*"
            onChange={handleFileChange}
          />
        </Button>
        <Typography
          variant="caption"
          display="block"
          color="text.secondary"
          sx={{ mt: 1 }}
        >
          PNG, JPG máximo 2MB
        </Typography>
      </Box>
    </Box>
  );
};
