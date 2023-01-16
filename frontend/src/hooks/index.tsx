import { useState } from "react";

function useStorage(key: string): [string, (name: string) => void] {
  const initial_value =
    window.localStorage.getItem(key) == null
      ? ""
      : window.localStorage.getItem(key);
  const [value, setValue] = useState<string>(initial_value as string);

  return [
    value,
    (newValue: string) => {
      window.localStorage.setItem(key, newValue);
      setValue(newValue);
    },
  ];
}

export function useUsername(): [string, (name: string) => void] {
  return useStorage("username");
}

export function useGameId(): [string, (name: string) => void] {
  return useStorage("gameId");
}
