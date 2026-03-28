
import api from '../../../api/axios/axiosConfig';
import type { ApiResponseSuccess } from '../../../common/interfaces/common';
import type { AuditManualResponse, ManualRecord, RefineManualResponse } from '../interfaces/ManualGeneratorData';
import type { GenerateManualInputs } from '../schemas/generarManual';
export const manualGeneratorService = {

  auditManual: async (idBrand:string,raw_parameters: GenerateManualInputs): Promise<AuditManualResponse| ManualRecord> => {
    try {
      console.log(raw_parameters)
      const response = await api.post<ApiResponseSuccess<AuditManualResponse| ManualRecord>>(`/manual_generator/audit/${idBrand}`,raw_parameters);
      
      if (response.data.success) {
        console.log({data:response.data.data})
        return response.data.data; 
      } else {
       
        throw new Error(response.data.message || "Error al registrar auditar parametros del manual");
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
      console.error("BrandService Error:", errorMessage);
      throw new Error(errorMessage);
    }
  },

  refineManual: async (manualId:string,refinement_prompt: string): Promise<AuditManualResponse| ManualRecord> => {
    try {
      console.log(refinement_prompt)
      const response = await api.post<ApiResponseSuccess<AuditManualResponse| ManualRecord>>(`/manual_generator/refine/${manualId}`,{ refinement_prompt });
      
      if (response.data.success) {
        console.log({data:response.data.data})
        return response.data.data; 
      } else {
       
        throw new Error(response.data.message || "Error al registrar nueva marca");
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
      console.error("BrandService Error:", errorMessage);
      throw new Error(errorMessage);
    }
  },
  confirmManual: async (manualId:string,): Promise<RefineManualResponse> => {
    try {
      console.log({manualId})
      const response = await api.post<ApiResponseSuccess<RefineManualResponse>>(`/manual_generator/confirm/${manualId}`);
      
      if (response.data.success) {
        console.log({data:response.data.data})
        return response.data.data; 
      } else {
       
        throw new Error(response.data.message || "Error al registrar nueva marca");
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
      console.error("BrandService Error:", errorMessage);
      throw new Error(errorMessage);
    }
  },
};