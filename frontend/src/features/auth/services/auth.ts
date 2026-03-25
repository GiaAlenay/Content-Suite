
import { supabase } from "../../../api/supabase/supabase";
import type { LoginFormInputs } from '../../../common/utils/schemas';

export const authService = {
  login: async ({ email, password }: LoginFormInputs) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) throw new Error(error.message);
    return data;
  },

  logout: async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw new Error(error.message);
  },

  getCurrentUser: async () => {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
  }
};