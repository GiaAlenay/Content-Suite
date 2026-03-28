import { useMutation, useQueryClient } from "@tanstack/react-query";
import { StorageService } from "./uploadService";

export const useUpload = () => {
  const queryClient = useQueryClient();

  const uploadImageMutation = useMutation({
    mutationFn: ({ brandCode, file }: { brandCode: string; file: File }) =>
      StorageService.uploadImage(brandCode, file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["brands"] });
    },
  });

  return {
    uploadImage: uploadImageMutation.mutateAsync,
    isUploading: uploadImageMutation.isPending,
    uploadError: uploadImageMutation.error,
  };
};
