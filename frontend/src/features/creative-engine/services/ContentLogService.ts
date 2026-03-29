
import api from '../../../api/axios/axiosConfig';
import type { ApiResponseSuccess } from '../../../common/interfaces/common';
import type { ContentLogInterface } from '../interfaces/ContentLogData';
import type { GenerateContentInputs } from '../schemas/agregarContentLog';
export const contentLogService = {

  getAllMyContentLogs: async (): Promise<ContentLogInterface[]> => {
    try {
    
      const response = await api.get<ApiResponseSuccess<ContentLogInterface[]>>('/content_log/list_me');
      
      if (response.data.success) {
        console.log({data:response.data.data})
        return response.data.data; 
      } else {
       
        throw new Error(response.data.message || "Error al obtener las contenidos");
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
      console.error("contentLogService Error:", errorMessage);
      throw new Error(errorMessage);
    }
  },

  createContentLog: async (newBrand: GenerateContentInputs): Promise<ContentLogInterface> => {
    try {
      console.log(newBrand)
      const response = await api.post<ApiResponseSuccess<ContentLogInterface>>('/content_log/create',newBrand);
      
      if (response.data.success) {
        console.log({data:response.data.data})
        return response.data.data; 
      } else {
       
        throw new Error(response.data.message || "Error al registrar nueva contenido");
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
      console.error("contentLogService Error:", errorMessage);
      throw new Error(errorMessage);
    }
  },
};