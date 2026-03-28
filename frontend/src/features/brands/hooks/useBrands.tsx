// src/features/brands/hooks/useBrands.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { brandService } from "../services/BrandService";
import type { CreateBrandInputs } from "../schemas/agregarBrand";

export const useBrands = () => {
  const queryClient = useQueryClient();

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["brands"],
    queryFn: brandService.getAllBrands,
    staleTime: 1000 * 60 * 5,
  });

  const createBrandMutation = useMutation({
    mutationFn: (newBrand: CreateBrandInputs) =>
      brandService.createBrand(newBrand),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["brands"] });
    },
  });

  return {
    brands: data || [],
    isLoadingBrands: isLoading,
    isErrorBrands: isError,
    errorBrand: error,

    createBrand: createBrandMutation.mutateAsync,
    isCreating: createBrandMutation.isPending,
  };
};
