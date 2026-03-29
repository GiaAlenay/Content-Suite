import { useMemo, useState } from "react";
import { MainContentLayout } from "../../../common/layouts/MainContentLayout";
import { useContentLogs } from "../hooks/contentLogs";
import ContentLogFilters from "../components/TableContenLog/ContentLogFilters";
import type { ContentLogTableData } from "../interfaces/ContentLogData";
import { listaStatusDisponibles } from "../constants";
import { NoFilteredData } from "../../../common/components/NoData/NoFilteredData";
import { ContentLogTable } from "../components/TableContenLog/TableContenLog";
export const CreativeEnginePage = () => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("ACTIVE");

  const {
    contentLogs,
    isLoadingContentLogs,
    isErrorContentLogs,
    errorContentLog,
    createContentLog,
    isCreating,
  } = useContentLogs();

  const handleAddContentLog = () => {
    setIsAddModalOpen(true);
  };
  const handleOpenContentLog = (contentLog: ContentLogTableData) => {};
  const handleOpenShowMoreContenLog = (contentLog: ContentLogTableData) => {};

  const filteredContentLogs = useMemo(() => {
    console.log({ contentLogs });
    if (!contentLogs) return [];

    const lowerSearchTerm = searchTerm.toLowerCase().trim();

    return contentLogs.filter((contentLog) => {
      // 1. Buscador Universal: Iteramos por todos los valores del objeto
      const matchesSearch = Object.values(contentLog).some((value) => {
        // Solo buscamos si el valor es un string
        if (typeof value === "string") {
          return value.toLowerCase().includes(lowerSearchTerm);
        }
        return false;
      });

      // 2. Mantenemos el filtro por estado (lógica de negocio específica)
      const matchesStatus =
        statusFilter === "ALL" || contentLog.status === statusFilter;

      return matchesSearch;
    });
  }, [contentLogs, searchTerm, statusFilter]);

  return (
    <MainContentLayout
      title="Mi Espacio Creativo"
      onPlusClick={() => handleAddContentLog()}
      isLoading={isLoadingContentLogs}
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
            onGenerateContenLog={handleOpenContentLog}
            onWatchContentLog={handleOpenShowMoreContenLog}
          />
        )}
      </>
    </MainContentLayout>
  );
};
