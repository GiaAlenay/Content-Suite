import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { contentLogService } from "../services/ContentLogService";
import type { GenerateContentInputs } from "../schemas/agregarContentLog";
import type { ContentLogUpdateInputsInterface } from "../interfaces/ContentLogData";

export const useContentLogs = () => {
  const queryClient = useQueryClient();

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["contentLogs"],
    queryFn: contentLogService.getAllMyContentLogs,
    staleTime: 1000 * 60 * 5,
  });

  const createContentLogMutation = useMutation({
    mutationFn: ({
      brandId,
      newContentLog,
    }: {
      brandId: string;
      newContentLog: GenerateContentInputs;
    }) => contentLogService.createContentLog(brandId, newContentLog),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contentLogs"] });
    },
  });

  const updateContentLogMutation = useMutation({
    mutationFn: ({
      contentLogId,
      newContentLog,
    }: {
      contentLogId: string;
      newContentLog: ContentLogUpdateInputsInterface;
    }) => contentLogService.updateContentLog(contentLogId, newContentLog),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contentLogs"] });
    },
  });

  return {
    contentLogs: data || [],
    isLoadingContentLogs: isLoading,
    isErrorContentLogs: isError,
    errorContentLog: error,

    createContentLog: createContentLogMutation.mutateAsync,
    isCreating: createContentLogMutation.isPending,

    updateContentLog: updateContentLogMutation.mutateAsync,
    isUpdating: updateContentLogMutation.isPending,
  };
};
