// src/features/auth/components/LoginForm.tsx
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  TextField,
  Button,
  Box,
  Typography,
  Paper,
  InputAdornment,
  IconButton,
} from "@mui/material";
import { LoginSchema } from "../../../common/utils/schemas";
import type { LoginFormInputs } from "../../../common/utils/schemas";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { useState } from "react";
interface LoginFormProps {
  onSubmit: (data: LoginFormInputs) => void;
  isLoading: boolean;
}

export const LoginForm = ({ onSubmit, isLoading }: LoginFormProps) => {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormInputs>({
    resolver: zodResolver(LoginSchema),
    defaultValues: { email: "", password: "" },
  });

  const [showPassword, setShowPassword] = useState(false);
  const handleClickShowPassword = () => setShowPassword((show) => !show);
  return (
    <Paper
      elevation={3}
      sx={{
        p: 5,
        mx: "auto",
        width: "100%",
        maxWidth: "500px",
        borderRadius: 3,
        border: "1px solid rgba(0, 0, 0, 0.12)",
        boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch",
        }}
      >
        <Typography
          variant="h5"
          fontWeight="bold"
          textAlign="center"
          sx={{ mb: 3 }}
        >
          Inicio de Sesión
        </Typography>

        <Box
          component="form"
          onSubmit={handleSubmit(onSubmit)}
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 2,
          }}
        >
          {/* Campo Email */}
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 500, mb: 0.5 }}>
              Correo Electrónico
            </Typography>
            <Controller
              name="email"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  placeholder="example@hotmail.com"
                  fullWidth
                  error={!!errors.email}
                  helperText={errors.email?.message}
                  disabled={isLoading}
                />
              )}
            />
          </Box>

          {/* Campo Password */}
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 500, mb: 0.5 }}>
              Contraseña
            </Typography>
            <Controller
              name="password"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  placeholder="• • • • • • • •"
                  type={showPassword ? "text" : "password"}
                  error={!!errors.password}
                  helperText={errors.password?.message}
                  disabled={isLoading}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle password visibility"
                          onClick={handleClickShowPassword}
                          edge="end"
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              )}
            />
          </Box>

          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="medium" // Para que se vea más robusto como en tu imagen
            sx={{ py: 1.5 }}
            disabled={isLoading}
          >
            {isLoading ? "..." : "Iniciar Sesión"}
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};
