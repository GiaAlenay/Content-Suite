import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { contentLogService } from "../services/ContentLogService";
import type { GenerateContentInputs } from "../schemas/agregarContentLog";

export const useContentLogs = () => {
  const queryClient = useQueryClient();

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["contentLogs"],
    queryFn: contentLogService.getAllMyContentLogs,
    staleTime: 1000 * 60 * 5,
  });

  const createContentLogMutation = useMutation({
    mutationFn: (newContentLog: GenerateContentInputs) =>
      contentLogService.createContentLog(newContentLog),
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
  };
};
