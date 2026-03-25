import { useState } from "react";
import { LoginForm } from "../components/LoginForm";
import { Container } from "@mui/material";
// import type { LoginFormInputs } from "../../../common/utils/schemas";

export const LoginPage = () => {
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");

  const handleLogin = async () => {};

  return (
    <Container
      component="main"
      maxWidth="xs"
      sx={{
        minHeight: "90vh",
        verticalAlign: "middle",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <LoginForm onSubmit={handleLogin} isLoading={status === "loading"} />;
    </Container>
  );
};
