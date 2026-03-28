
import api from '../../../api/axios/axiosConfig';
import type { ApiResponseSuccess } from '../../../common/interfaces/common';
import type { BrandInterface } from '../interfaces/BrandData';
import type { CreateBrandInputs } from '../schemas/agregarBrand';
export const brandService = {

  getAllBrands: async (): Promise<BrandInterface[]> => {
    try {
    
      const response = await api.get<ApiResponseSuccess<BrandInterface[]>>('/brand/list');
      
      if (response.data.success) {
        console.log({data:response.data.data})
        return response.data.data; 
      } else {
       
        throw new Error(response.data.message || "Error al obtener las marcas");
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || "Error de conexión con el servidor";
      console.error("BrandService Error:", errorMessage);
      throw new Error(errorMessage);
    }
  },

  createBrand: async (newBrand: CreateBrandInputs): Promise<BrandInterface> => {
    try {
      console.log(newBrand)
      const response = await api.post<ApiResponseSuccess<BrandInterface>>('/brand/create',newBrand);
      
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