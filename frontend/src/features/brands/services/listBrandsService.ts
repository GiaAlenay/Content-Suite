
import api from '../../../api/axios/axiosConfig';
import type { ApiResponseSuccess } from '../../../common/interfaces/common';
import { BrandInterface } from '../interfaces/BrandData';
export const brandService = {
  /**
   * Obtiene el listado de marcas envolviendo la respuesta del backend
   */
  getAllBrands: async (): Promise<BrandInterface[]> => {
    try {
      // 1. Tipamos la respuesta completa de Axios
      const response = await api.get<ApiResponseSuccess<BrandInterface[]>>('/brands/list');
      
      // 2. Verificamos el flag 'success' que envía tu Backend
      if (response.data.success) {
        return response.data.data; // Retornamos solo el array de brands
      } else {
       
        throw new Error(response.data.message || "Error al obtener las marcas");
      }
    } catch (error: any) {
      // Manejo de errores de red o errores 4xx/5xx de FastAPI
      const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
      console.error("BrandService Error:", errorMessage);
      throw new Error(errorMessage);
    }
  },
};