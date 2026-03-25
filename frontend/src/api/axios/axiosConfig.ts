// src/api/axiosConfig.ts
import axios from 'axios';
import { supabase } from '../supabase/supabase';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000', // Tu URL de FastAPI
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(async (config) => {
  const { data } = await supabase.auth.getSession();
  const token = data.session?.access_token;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  return config;
});

export default api;