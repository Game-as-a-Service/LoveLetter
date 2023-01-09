import { useState } from "react";

export function useUsername(): [string, (name: string) => void] {
  const initial_username =
    window.localStorage.getItem("username") == null
      ? ""
      : window.localStorage.getItem("username");
  const [username, setUsername] = useState<string>(initial_username as string);

  return [
    username,
    (newUsername: string) => {
      window.localStorage.setItem("username", newUsername);
      setUsername(newUsername);
    },
  ];
}
