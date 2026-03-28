import { useMutation, useQueryClient } from "@tanstack/react-query";

import { manualGeneratorService } from "../services/ManualGeneratorService";
import type { GenerateManualInputs } from "../schemas/generarManual";

export const useManualGenerator = () => {
  const queryClient = useQueryClient();

  const auditManualMutation = useMutation({
    mutationFn: ({
      idBrand,
      raw_parameters,
    }: {
      idBrand: string;
      raw_parameters: GenerateManualInputs;
    }) => manualGeneratorService.auditManual(idBrand, raw_parameters),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["manual_generator"] });
    },
  });

  const refineManualMutation = useMutation({
    mutationFn: ({
      manualId,
      refinement_prompt,
    }: {
      manualId: string;
      refinement_prompt: string;
    }) => manualGeneratorService.refineManual(manualId, refinement_prompt),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["manual_generator"] });
    },
  });
  const confirmManualMutation = useMutation({
    mutationFn: (manualId: string) =>
      manualGeneratorService.confirmManual(manualId),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["brands", "manual_generator"],
      });
    },
  });

  return {
    auditManual: auditManualMutation.mutateAsync,
    isAuditing: auditManualMutation.isPending,
    refineManual: refineManualMutation.mutateAsync,
    isRefining: refineManualMutation.isPending,
    confirmManual: confirmManualMutation.mutateAsync,
    isConfirming: confirmManualMutation.isPending,
  };
};
