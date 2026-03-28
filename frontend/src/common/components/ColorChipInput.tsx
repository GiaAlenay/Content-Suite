import { useState } from "react";
import { Stack, TextField, Chip, Box, Typography } from "@mui/material";
import { IconPalette, IconPlus } from "@tabler/icons-react";

interface ColorChipInputProps {
  colors: string[];
  onChange: (colors: string[]) => void;
  error?: boolean;
}

export const ColorChipInput = ({
  colors,
  onChange,
  error,
}: ColorChipInputProps) => {
  const [inputValue, setInputValue] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);

  const validateHex = (hex: string) =>
    /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hex);

  const handleAddColor = () => {
    const hex = inputValue.startsWith("#") ? inputValue : `#${inputValue}`;

    if (!validateHex(hex)) {
      setLocalError("Formato HEX inválido (ej: #0047AB)");
      return;
    }

    if (colors.includes(hex)) {
      setLocalError("El color ya existe");
      return;
    }

    onChange([...colors, hex]);
    setInputValue("");
    setLocalError(null);
  };

  return (
    <Stack spacing={1}>
      <TextField
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={(e) =>
          e.key === "Enter" && (e.preventDefault(), handleAddColor())
        }
        placeholder="Ej: #0047AB o FFFFFF"
        error={!!localError || error}
        helperText={localError}
        InputProps={{
          startAdornment: (
            <IconPalette size={18} style={{ marginRight: 8, opacity: 0.5 }} />
          ),
          endAdornment: (
            <IconPlus
              size={20}
              style={{ cursor: "pointer", opacity: inputValue ? 1 : 0.3 }}
              onClick={handleAddColor}
            />
          ),
        }}
      />
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1, mt: 1 }}>
        {colors.map((color) => (
          <Chip
            key={color}
            label={color}
            onDelete={() => onChange(colors.filter((c) => c !== color))}
            sx={{
              bgcolor: color,
              color:
                parseInt(color.replace("#", ""), 16) > 0xffffff / 2
                  ? "#000"
                  : "#fff",
              fontWeight: "bold",
              border: "1px solid rgba(0,0,0,0.1)",
            }}
          />
        ))}
      </Box>
    </Stack>
  );
};
