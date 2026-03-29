import { useState } from "react";
import { BrandTable } from "../components/TableBrand/TableBrand";
import BrandFilters from "../components/TableBrand/BrandFilters";
import type { BrandTableData } from "../interfaces/BrandData";
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
import { NoFilteredData } from "../../../common/components/NoData/NoFilteredData";
import { useNavigate } from "react-router-dom";
import { MainContentLayout } from "../../../common/layouts/MainContentLayout";

export const BrandsPage = () => {
  const {
    brands,
    isLoadingBrands,
    isErrorBrands,
    errorBrand,
    createBrand,
    isCreating,
  } = useBrands();
  const navigate = useNavigate();
  const { uploadImage, isUploading } = useUpload();

  const [searchTerm, setSearchTerm] = useState("");

  const [selectedBrand, setSelectedBrand] = useState<BrandTableData | null>(
    null,
  );
  const [isConfirmDeleteOpen, setIsConfirmDeleteOpen] = useState(false);
  const [file, setFile] = useState<File | null>(null);

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  const filteredBrands: BrandTableData[] = brands?.filter((brand) => {
    const matchesSearch =
      brand.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      brand.code.toLowerCase().includes(searchTerm.toLowerCase());

    return matchesSearch;
  });

  const handleAddBrand = () => {
    setIsAddModalOpen(true);
  };

  const handleSaveNewBrand = async (
    data: CreateBrandInputs,
    onSuccess: () => void,
  ) => {
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
    navigate(`/brands/${brand.id}/generate-manual`);
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

  return (
    <MainContentLayout
      title="Marcas"
      onPlusClick={() => handleAddBrand()}
      isLoading={isLoadingBrands}
      isError={isErrorBrands}
      isEmpty={brands?.length === 0}
      errorMsg={(errorBrand as Error)?.message ?? null}
      emptyLabel="marcas"
    >
      <>
        <BrandFilters searchValue={searchTerm} setSearchValue={setSearchTerm} />

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
    </MainContentLayout>
  );
};
