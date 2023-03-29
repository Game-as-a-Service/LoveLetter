import { useState } from "react";

export function useLocalStorage(key: string) {
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
  ] as const;
}
