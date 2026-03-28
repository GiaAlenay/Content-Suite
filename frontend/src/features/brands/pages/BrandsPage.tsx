import { useState } from "react";
import { Box, Typography, Button, Stack } from "@mui/material";
import { BrandTable } from "../components/TableBrand/TableBrand";
import BrandFilters from "../components/TableBrand/BrandFilters";
import type { BrandTableData } from "../interfaces/BrandData";
import { GenerateManualModal } from "../components/GenerarManual/ModalGenerarManual";
import { IconPlus, IconSearchOff } from "@tabler/icons-react";
import type { CreateBrandInputs } from "../schemas/agregarBrand";
import { AddBrandModal } from "../components/AddBrand/AddBrand";
import { ConfirmActionModal } from "../../../common/components/ConfirmActionModal/ConfirmActionModal";
import { useBrands } from "../hooks/useBrands";
import NotificationService from "../../../common/utils/Notification";
import { useUpload } from "../../../common/components/StorageService/uploadQuery";
import {
  deactivateDescript,
  deactivateTitle,
} from "../constants/confirmDeleteModalContent";
import { Loader } from "../../../common/components/Loader/Loader";
import { ErrorContent } from "../../../common/components/ErrorContent/ErrorContent";
import { NoRawData } from "../../../common/components/NoData/NoRawData";
import { NoFilteredData } from "../../../common/components/NoData/NoFilteredData";

export const BrandsPage = () => {
  const {
    brands,
    isLoadingBrands,
    isErrorBrands,
    errorBrand,
    createBrand,
    isCreating,
  } = useBrands();

  const { uploadImage, isUploading } = useUpload();

  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("ACTIVE");

  const [selectedBrand, setSelectedBrand] = useState<BrandTableData | null>(
    null,
  );
  const [isManualModalOpen, setIsManualModalOpen] = useState(false);
  const [isConfirmDeleteOpen, setIsConfirmDeleteOpen] = useState(false);
  const [file, setFile] = useState<File | null>(null);

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  const filteredBrands: BrandTableData[] = brands?.filter((brand) => {
    const matchesSearch =
      brand.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      brand.code.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus =
      statusFilter === "ALL" || brand.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleAddBrand = () => {
    setIsAddModalOpen(true);
  };

  const handleSaveNewBrand = async (
    data: CreateBrandInputs,
    onSuccess: () => void,
  ) => {
    console.log(file);
    if (!file) return;
    try {
      const uploadResponse = await uploadImage({
        brandCode: data.code,
        file: file,
      });
      if (!uploadResponse) throw new Error("Error al cargar el Logo.");

      await createBrand({ ...data, logo_url: uploadResponse });
      NotificationService.showSuccessAlertPersonalizado(
        "Nueva marca registrada",
        "Se registro la nueva Marca correctamente",
        () => {
          setIsAddModalOpen(false);
          onSuccess();
        },
      );
    } catch (err: any) {
      NotificationService.showErrorssAlertPersonalizado(
        "Error al Registrar nueva Marca",
        err.error,
      );
    }
  };

  const handleOpenManual = (brand: BrandTableData) => {
    setSelectedBrand(brand);
    setIsManualModalOpen(true);
  };

  const handleCloseManual = () => {
    setIsManualModalOpen(false);
    setSelectedBrand(null);
  };

  const handleOpenConfirmDelete = (brand: BrandTableData) => {
    setSelectedBrand(brand);
    setIsConfirmDeleteOpen(true);
  };

  const handleCloseConfirmDelete = () => {
    setIsConfirmDeleteOpen(false);
    setSelectedBrand(null);
  };

  const handleConfirm = async () => {};
  let mainContent;

  if (isLoadingBrands) mainContent = <Loader />;
  else if (isErrorBrands)
    mainContent = <ErrorContent msg={(errorBrand as Error).message} />;
  else if (brands.length === 0) mainContent = <NoRawData itemsName="marcas" />;
  else
    mainContent = (
      <>
        <BrandFilters
          status={statusFilter}
          setStatus={setStatusFilter}
          searchValue={searchTerm}
          setSearchValue={setSearchTerm}
          listaStatusDisponibles={["Activo", "Inactivo"]}
        />

        {filteredBrands.length === 0 ? (
          <NoFilteredData itemsName="marcas" />
        ) : (
          <BrandTable
            data={filteredBrands}
            onGenerateManual={handleOpenManual}
            onDeleteBrand={handleOpenConfirmDelete}
          />
        )}
      </>
    );
  return (
    <Box
      sx={{
        padding: "24px 32px",
        borderRadius: "8px",
        background: "#fff",
        border: "1px solid rgba(0, 0, 0, 0.12)",
        boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
        minHeight: "800px",
      }}
    >
      <div
        className="w-100 column-base"
        style={{ padding: "24px", gap: "24px", minHeight: "100%" }}
      >
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography variant="h4" fontWeight="bold">
            Marcas
          </Typography>
          <Button
            variant="contained"
            startIcon={<IconPlus />}
            onClick={handleAddBrand}
            sx={{
              borderRadius: "50%",
              height: "48px",
              minWidth: "48px",
              padding: 0,
              "& .MuiButton-startIcon": {
                margin: 0,
              },
            }}
          />
        </Stack>

        {mainContent}

        {selectedBrand && isManualModalOpen && (
          <GenerateManualModal
            open={isManualModalOpen}
            onClose={handleCloseManual}
            brandName={selectedBrand.name}
          />
        )}
        {selectedBrand && isConfirmDeleteOpen && (
          <ConfirmActionModal
            open={isConfirmDeleteOpen}
            onClose={handleCloseConfirmDelete}
            onConfirm={handleConfirm}
            title={deactivateTitle}
            description={deactivateDescript(selectedBrand.name)}
            loading={isLoadingBrands}
          />
        )}

        <AddBrandModal
          open={isAddModalOpen}
          onClose={() => setIsAddModalOpen(false)}
          onSave={handleSaveNewBrand}
          isLoading={isCreating || isUploading}
          setFile={(file: File) => setFile(file)}
        />
      </div>
    </Box>
  );
};
