import { useState } from "react";
import { LoginForm } from "../components/LoginForm";
import { Alert, Box } from "@mui/material";
import type { LoginFormInputs } from "../../../common/utils/schemas";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../common/contexts/useAuth";

export const LoginPage = () => {
  const navigate = useNavigate();
  const { signIn } = useAuth();

  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleLogin = async (data: LoginFormInputs) => {
    console.log("esta en login");
    setIsLoading(true);
    setErrorMessage(null);

    try {
      await signIn(data);

      navigate("/brands");
    } catch (error: any) {
      setErrorMessage(error.message || "Ocurrió un error al iniciar sesión");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "#ddddddff",
      }}
    >
      <Box sx={{ width: "100%", maxWidth: "400px", px: 2 }}>
        {errorMessage && (
          <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>
            {errorMessage}
          </Alert>
        )}

        <LoginForm onSubmit={handleLogin} isLoading={isLoading} />
      </Box>
    </Box>
  );
};
