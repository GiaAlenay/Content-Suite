import { createContext } from "react";
import type { AuthContextType } from "../interfaces/common";

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined,
);
