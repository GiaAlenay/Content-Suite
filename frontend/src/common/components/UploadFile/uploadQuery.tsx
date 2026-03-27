import { useMutation, useQueryClient } from "@tanstack/react-query";
import { uploadService } from "./uploadService";

export const useUpload = () => {
  const queryClient = useQueryClient();

  const uploadImageMutation = useMutation({
    mutationFn: ({ brandCode, file }: { brandCode: string; file: File }) =>
      uploadService.uploaImage(brandCode, file),
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
