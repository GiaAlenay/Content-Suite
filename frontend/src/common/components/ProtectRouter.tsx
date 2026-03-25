// src/common/components/ProtectedRoute.tsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../contexts/useAuth";
import { CircularProgress, Box } from "@mui/material";

export const ProtectedRoute = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 10 }}>
        <CircularProgress color="primary" /> {/* Tu naranja global */}
      </Box>
    );
  }

  return user ? <Outlet /> : <Navigate to="/login" replace />;
};
