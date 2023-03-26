import { useLocalStorage } from "./useLocalStorage";

export function useUsername(): ReturnType<typeof useLocalStorage> {
  return useLocalStorage("username");
}
