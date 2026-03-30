// src/features/brands/hooks/useBrands.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { brandService } from "../services/BrandService";
import type { CreateBrandInputs } from "../schemas/agregarBrand";

export const useBrands = () => {
  const queryClient = useQueryClient();

  const {
    data: brandsData,
    isLoading: isLoadingBrands,
    isError: isErrorBrands,
    error: errorBrand,
  } = useQuery({
    queryKey: ["brands", "all"],
    queryFn: brandService.getAllBrands,
    staleTime: 1000 * 60 * 5,
  });

  const {
    data: activeBrandsData,
    isLoading: isLoadingBrandsActiveManual,
    isError: isErrorBrandsActiveManual,
    error: errorBrandActiveManual,
  } = useQuery({
    queryKey: ["brands", "active-manual"],
    queryFn: brandService.getAllActiveBrandsWithManual,
    staleTime: 1000 * 60 * 5,
  });

  const createBrandMutation = useMutation({
    mutationFn: (newBrand: CreateBrandInputs) =>
      brandService.createBrand(newBrand),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["brands"] });
    },
  });

  const deleteBrandMutation = useMutation({
    mutationFn: (brandId: string) => brandService.deleteBrand(brandId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["brands"] });
    },
  });

  return {
    brands: brandsData || [],
    isLoadingBrands,
    isErrorBrands,
    errorBrand,

    brandsActiveManual: activeBrandsData || [],
    isLoadingBrandsActiveManual,
    isErrorBrandActiveManual: isErrorBrandsActiveManual,
    errorBrandActiveManual: errorBrandActiveManual,

    createBrand: createBrandMutation.mutateAsync,
    isCreating: createBrandMutation.isPending,

    deleteBrand: deleteBrandMutation.mutateAsync,
    isDeleting: deleteBrandMutation.isPending,
  };
};
