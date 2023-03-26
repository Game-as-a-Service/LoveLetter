import { useLocalStorage } from "./useLocalStorage";

export function useGameId(): ReturnType<typeof useLocalStorage> {
  return useLocalStorage("gameId");
}
