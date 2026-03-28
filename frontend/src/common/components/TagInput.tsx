import { useState } from "react";
import { Stack, TextField, Chip, Box } from "@mui/material";
import { IconTag } from "@tabler/icons-react";

interface TagInputProps {
  placeholder: string;
  tags: string[];
  onChange: (tags: string[]) => void;
  error?: boolean;
  color?: "primary" | "error";
}

export const TagInput = ({
  placeholder,
  tags,
  onChange,
  error,
  color = "primary",
}: TagInputProps) => {
  const [inputValue, setInputValue] = useState("");

  const handleAddTag = () => {
    const trimmed = inputValue.trim();
    if (trimmed && !tags.includes(trimmed)) {
      onChange([...tags, trimmed]);
      setInputValue("");
    }
  };

  return (
    <Stack spacing={1}>
      {/* <Typography
        variant="caption"
        fontWeight="bold"
        color={error ? "error" : "text.secondary"}
      >
        {label}
      </Typography> */}
      <TextField
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={(e) =>
          e.key === "Enter" && (e.preventDefault(), handleAddTag())
        }
        placeholder={placeholder}
        error={error}
        InputProps={{
          startAdornment: (
            <IconTag size={18} style={{ marginRight: 8, opacity: 0.5 }} />
          ),
        }}
      />
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
        {tags.map((tag) => (
          <Chip
            key={tag}
            label={tag}
            color={color}
            variant="outlined"
            onDelete={() => onChange(tags.filter((t) => t !== tag))}
            sx={{ borderRadius: "8px" }}
          />
        ))}
      </Box>
    </Stack>
  );
};
