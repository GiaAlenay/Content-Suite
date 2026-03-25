import { LoginPage } from "./features/auth/pages/LoginPages";
import { BrandsPage } from "./features/brands/pages/BrandsPage";
import { CreativeEnginePage } from "./features/creative-engine/pages/CreativeEnginePage";
import { GovernancePage } from "./features/governance/pages/GovernancePage";
import { DashboardLayout } from "./common/layouts/DashboardLayout";
import "./App.css";
import { Routes, Route, Navigate } from "react-router-dom";
import { ProtectedRoute } from "./common/components/ProtectRouter";
function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>
          <Route path="/brands" element={<BrandsPage />} />
          <Route path="/creative-engine" element={<CreativeEnginePage />} />
          <Route path="/governance" element={<GovernancePage />} />

          <Route path="/" element={<Navigate to="/brands" replace />} />
        </Route>

        <Route path="*" element={<div>Página no encontrada</div>} />
      </Route>
    </Routes>
  );
}

export default App;
