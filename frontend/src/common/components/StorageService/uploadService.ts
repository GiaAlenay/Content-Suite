import api from "../../../api/axios/axiosConfig";

export const StorageService = {
 

  uploadImage: async (brandCode: string, file: File): Promise<string> => {
    try {
      const formData = new FormData();
      formData.append("file", file); 
      const response = await api.post<{ image_url: string }>(
        `/upload/upload-imagen/${brandCode}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      return response.data.image_url;
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || "Error al subir la imagen";
      throw new Error(errorMessage);
    }
  },
};