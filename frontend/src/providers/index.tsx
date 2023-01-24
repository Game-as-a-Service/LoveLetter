import { GameStatus } from "@/types";
import { createContext, ReactNode, useEffect, useMemo, useState } from "react";
import { useGameId, useUsername } from "@/hooks";
import { GetGameStatus } from "@/apis";
import { isEqual } from "lodash";
import { border } from "@chakra-ui/react";

export interface GameInformation {
  gameId: string;
  gameStatus: GameStatus | null;
  IsReady: () => boolean;
  GetUsername: () => string;
}

export const GameContext = createContext<GameInformation>({
  GetUsername(): string {
    return "";
  },
  IsReady(): boolean {
    return false;
  },
  gameId: "",
  gameStatus: null,
});

interface GameDataProviderProps {
  children: ReactNode;
}

export function GameDataProvider(props: GameDataProviderProps) {
  const [gameId] = useGameId();
  const [username] = useUsername();
  const [gameStatus, setGameStatus] = useState<GameStatus | null>(null);

  // refresh GameStatus every 1 second.
  useEffect(() => {
    // set GameStatus before the refresher triggered
    GetGameStatus(gameId, username).then((status: GameStatus) => {
      if (!isEqual(gameStatus, status)) {
        setGameStatus(status);
      }
    });

    const intervalId = setInterval(() => {
      // auto-refresh GameStatus
      GetGameStatus(gameId, username).then((status: GameStatus) => {
        if (!isEqual(gameStatus, status)) {
          setGameStatus(status);
        }
      });
    }, 1 * 1000);
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  const value: GameInformation = {
    gameId,
    gameStatus,
    IsReady: (): boolean => {
      return gameStatus != null;
    },
    GetUsername: () => username,
  };
  return (
    <GameContext.Provider value={value}>{props.children}</GameContext.Provider>
  );
}
