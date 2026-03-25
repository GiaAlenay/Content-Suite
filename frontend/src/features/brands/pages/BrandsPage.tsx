import { useState } from "react";
import { Box, Typography, Button, Stack } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { BrandTable } from "../components/TableBrand";
import BrandFilters from "../components/table/BrandFilters";
import type { BrandTableData } from "../interfaces/BrandData";
import { GenerateManualModal } from "../components/ModalGenerarManual";

const MOCK_BRANDS: any = [
  {
    id: 1,
    code: "BRD-001",
    name: "TechFlow",
    logo_url: "https://via.placeholder.com/40",
    status: "ACTIVE",
    description: "Soluciones tecnológicas",
  },
  {
    id: 2,
    code: "BRD-002",
    name: "EcoGreen",
    logo_url: "https://via.placeholder.com/40",
    status: "INACTIVE",
    description: "Productos sustentables",
  },
  {
    id: 3,
    code: "BRD-003",
    name: "NovaSoft",
    logo_url: "https://via.placeholder.com/40",
    status: "ACTIVE",
    description: "Software factory",
  },
];

export const BrandsPage = () => {
  // Estados para filtros
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("ACTIVE");

  const [selectedBrand, setSelectedBrand] = useState<BrandTableData | null>(
    null,
  );
  const [isManualModalOpen, setIsManualModalOpen] = useState(false);

  const handleOpenManual = (brand: BrandTableData) => {
    setSelectedBrand(brand);
    setIsManualModalOpen(true);
  };

  const handleCloseManual = () => {
    setIsManualModalOpen(false);
    setSelectedBrand(null);
  };

  const handleAddBrand = () => {
    console.log("Abrir modal de creación");
  };

  return (
    <Box
      sx={{
        padding: "24px 32px",
        borderRadius: "8px",
        background: "#fff",
        border: "1px solid rgba(0, 0, 0, 0.12)",
        boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
      }}
    >
      <div
        className="w-100 column-base"
        style={{ padding: "24px", gap: "20px" }}
      >
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography variant="h4" fontWeight="bold">
            Brands
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddBrand}
            sx={{ height: "48px" }}
          ></Button>
        </Stack>

        <BrandFilters
          status={statusFilter}
          setStatus={setStatusFilter}
          searchValue={searchTerm}
          setSearchValue={setSearchTerm}
          listaStatusDisponibles={["Activo", "Inactivo"]}
        />

        <BrandTable data={MOCK_BRANDS} onGenerateManual={handleOpenManual} />

        {selectedBrand && (
          <GenerateManualModal
            open={isManualModalOpen}
            onClose={handleCloseManual}
            brandName={selectedBrand.name}
          />
        )}
      </div>
    </Box>
  );
};
