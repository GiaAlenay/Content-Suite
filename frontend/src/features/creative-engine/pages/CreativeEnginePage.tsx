import { useMemo, useState } from "react";
import { MainContentLayout } from "../../../common/layouts/MainContentLayout";
import { useContentLogs } from "../hooks/contentLogs";
import ContentLogFilters from "../components/TableContenLog/ContentLogFilters";
import type { ContentLogTableData } from "../interfaces/ContentLogData";
import {
  auditarRequestQuestion,
  auditarRequestTitle,
  listaStatusDisponibles,
} from "../constants";
import { NoFilteredData } from "../../../common/components/NoData/NoFilteredData";
import { ContentLogTable } from "../components/TableContenLog/TableContenLog";
import { ContentLogDetailModal } from "../components/Detalles";
import { AddContentLogModal } from "../components/AddContenLog/AddContentLog";
import { useBrands } from "../../brands/hooks/useBrands";
import { ConfirmActionModal } from "../../../common/components/ConfirmActionModal/ConfirmActionModal";
import NotificationService from "../../../common/utils/Notification";
import type { GenerateContentInputs } from "../schemas/agregarContentLog";

export const CreativeEnginePage = () => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [selectedContentLog, setSelectedContentLog] =
    useState<ContentLogTableData | null>(null);
  const [isConfirmCambiarStatusOpen, setIsConfirmCambiarStatusOpen] =
    useState(false);
  const [isDetailOpen, setIsDetailOpen] = useState(false);

  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const { brandsActiveManual, isLoadingBrandsActiveManual } = useBrands();

  const {
    contentLogs,
    isLoadingContentLogs,
    isErrorContentLogs,
    errorContentLog,
    createContentLog,
    isCreating,
    updateContentLog,
    isUpdating,
  } = useContentLogs();

  const handleAddContentLog = () => {
    setIsAddModalOpen(true);
  };

  const handleCloseAddContentLog = () => {
    setIsAddModalOpen(false);
  };

  const handleOpenDetail = (contentLog: ContentLogTableData) => {
    setSelectedContentLog(contentLog);
    setIsDetailOpen(true);
  };

  const handleCloseDetail = () => {
    setSelectedContentLog(null);
    setIsDetailOpen(false);
  };
  const filteredContentLogs = useMemo(() => {
    console.log({ contentLogs });
    if (!contentLogs) return [];

    const lowerSearchTerm = searchTerm.toLowerCase().trim();

    return contentLogs.filter((contentLog) => {
      const matchesSearch = Object.values(contentLog).some((value) => {
        if (typeof value === "string") {
          return value.toLowerCase().includes(lowerSearchTerm);
        }
        return false;
      });

      const matchesStatus =
        statusFilter === "ALL" || contentLog.status === statusFilter;

      return matchesSearch;
    });
  }, [contentLogs, searchTerm, statusFilter]);

  const handleSaveNewContentLog = async (
    data: GenerateContentInputs,
    action: () => void,
  ) => {
    try {
      const response = await createContentLog({
        brandId: data.brand_id,
        newContentLog: data,
      });

      return response;
    } catch (err: any) {
      if (err.status !== 400) {
        NotificationService.showErrorssAlertPersonalizado(
          "Error en el motor creativo",
          err.message,
        );
      }
      throw err;
    }
  };

  const handleConfirm = async (contentLogId?: string | null) => {
    try {
      if (!contentLogId) throw new Error("Id no habilitado");

      await updateContentLog({
        contentLogId,
        newContentLog: { status: "PENDING" },
      });
      NotificationService.showSuccessAlertPersonalizado(
        "Solcitud de auditoria registrada",
        "Se registro la solicitud de auditoria para tu contenido",
        () => {
          setIsAddModalOpen(false);
        },
      );
    } catch (err: any) {
      NotificationService.showErrorssAlertPersonalizado(
        "Error al solicitar auditoria",
        err.error,
      );
    }
  };

  const handleCloseConfirmCambiarStatus = () => {
    setIsConfirmCambiarStatusOpen(false);
    setSelectedContentLog(null);
  };

  const handleOpenConfirmCambiarStatus = (contentLog: ContentLogTableData) => {
    setIsConfirmCambiarStatusOpen(true);
    setSelectedContentLog(contentLog);
  };

  return (
    <MainContentLayout
      title="Mi Espacio Creativo"
      onPlusClick={() => handleAddContentLog()}
      isLoading={isLoadingContentLogs || isLoadingBrandsActiveManual}
      isError={isErrorContentLogs}
      isEmpty={contentLogs?.length === 0}
      errorMsg={(errorContentLog as Error)?.message ?? null}
      emptyLabel="marcas"
    >
      <>
        <ContentLogFilters
          status={statusFilter}
          setStatus={setStatusFilter}
          searchValue={searchTerm}
          setSearchValue={setSearchTerm}
          listaStatusDisponibles={listaStatusDisponibles}
        />
        {filteredContentLogs.length === 0 ? (
          <NoFilteredData itemsName="contenido" />
        ) : (
          <ContentLogTable
            data={filteredContentLogs}
            onUpdateStatusContenLog={handleOpenConfirmCambiarStatus}
            onWatchContentLog={handleOpenDetail}
          />
        )}

        {selectedContentLog && isDetailOpen && (
          <ContentLogDetailModal
            open={isDetailOpen}
            onClose={handleCloseDetail}
            contentLog={selectedContentLog}
          />
        )}

        <AddContentLogModal
          open={isAddModalOpen}
          onClose={handleCloseAddContentLog}
          brands={brandsActiveManual}
          onSave={handleSaveNewContentLog}
          isLoading={isCreating || isUpdating}
          handleConfirm={(contentLogId?: string | null) =>
            handleConfirm(contentLogId)
          }
        />

        {selectedContentLog &&
          isConfirmCambiarStatusOpen &&
          !isAddModalOpen && (
            <ConfirmActionModal
              open={isConfirmCambiarStatusOpen}
              onClose={handleCloseConfirmCambiarStatus}
              handleConfirm={() => handleConfirm(selectedContentLog.id)}
              title={auditarRequestTitle}
              description={auditarRequestQuestion}
              loading={isLoadingBrandsActiveManual || isCreating || isUpdating}
            />
          )}
      </>
    </MainContentLayout>
  );
};
