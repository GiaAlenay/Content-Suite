
import api from '../../../api/axios/axiosConfig';
import type { ApiResponseSuccess } from '../../../common/interfaces/common';
import type { AuditPromptResponse, ContentLogInterface, ContentLogUpdateInputsInterface } from '../interfaces/ContentLogData';
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

  createContentLog: async (brandId: string,newContentLog: GenerateContentInputs, ): Promise<ContentLogInterface | AuditPromptResponse> => {
  try {
    const response = await api.post<ApiResponseSuccess<ContentLogInterface | AuditPromptResponse>>(
      `/content_log/create/${brandId}`, 
      newContentLog
    );
    
    if (response.data.success) {
      return response.data.data; 
    } else {
      throw new Error(response.data.message || "Error al registrar nuevo contenido");
    }
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
    throw new Error(errorMessage);
  }
},

updateContentLog: async (contentLogId: string,newContentLog: ContentLogUpdateInputsInterface, ): Promise<ContentLogInterface | null> => {
  try {
    const response = await api.put<ApiResponseSuccess<ContentLogInterface | null>>(
      `/content_log/update/${contentLogId}`, 
      newContentLog
    );
    
    if (response.data.success) {
      return response.data.data; 
    } else {
      throw new Error(response.data.message || "Error al registrar cambios");
    }
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
    throw new Error(errorMessage);
  }
},
};