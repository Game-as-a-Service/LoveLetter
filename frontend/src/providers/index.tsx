import { getGameStatus } from "@/apis";
import { useGameId, useUsername } from "@/hooks";
import { GameStatus, TurnPlayer } from "@/types";
import { isEqual } from "lodash";
import { createContext, ReactNode, useEffect, useMemo, useState } from "react";

export interface GameInformation {
  getGameId: () => string;
  getGameStatus: () => GameStatus;

  isReady: () => boolean;
  getUsername: () => string;

  getTurnPlayer: () => TurnPlayer;

  isMyTurn: () => boolean;
  getStartPlayer: () => string;
  isGameOver: () => boolean;
}

class BeforeReadyGameInformation implements GameInformation {
  unknown = "<unknown>";

  getTurnPlayer(): TurnPlayer {
    return { cards: [], name: "unknown", out: false };
  }

  getUsername(): string {
    return this.unknown;
  }

  isReady(): boolean {
    return false;
  }

  getGameId(): string {
    return this.unknown;
  }

  getGameStatus(): GameStatus {
    return {
      events: [],
      game_id: "",
      players: [],
      rounds: [],
      final_winner: "",
    };
  }

  isMyTurn(): boolean {
    return false;
  }

  getStartPlayer(): string {
    return this.unknown;
  }

  isGameOver(): boolean {
    return false;
  }
}

class ConcreteGameInformation implements GameInformation {
  constructor(gameId: string, username: string, gameStatus: GameStatus) {
    this.gameId = gameId;
    this.username = username;
    this.gameStatus = gameStatus;
  }

  getGameId(): string {
    return this.gameId;
  }

  getGameStatus(): GameStatus {
    return this.gameStatus;
  }

  getTurnPlayer(): TurnPlayer {
    if (this.gameStatus.rounds.length === 0) {
      return { cards: [], name: "unknown", out: false };
    }
    return this.gameStatus.rounds[this.gameStatus.rounds.length - 1]
      .turn_player;
  }

  getUsername(): string {
    return this.username;
  }

  isReady(): boolean {
    return this.gameStatus != null;
  }

  isMyTurn(): boolean {
    return this.getTurnPlayer().name === this.username;
  }

  getStartPlayer(): string {
    if (this.gameStatus.rounds.length === 0) {
      return "<unknown>";
    }

    return this.gameStatus.rounds[this.gameStatus.rounds.length - 1]
      .start_player;
  }

  isGameOver(): boolean {
    return (
      this.gameStatus.final_winner != "" && this.gameStatus.final_winner != null
    );
  }

  gameId: string;
  username: string;
  gameStatus: GameStatus;
}

export const GameContext = createContext<GameInformation>(
  new BeforeReadyGameInformation()
);

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
    getGameStatus(gameId, username).then((status: GameStatus) => {
      if (!isEqual(gameStatus, status)) {
        setGameStatus(status);
      }
    });

    const intervalId = setInterval(() => {
      // auto-refresh GameStatus
      getGameStatus(gameId, username).then((status: GameStatus) => {
        if (!isEqual(gameStatus, status)) {
          setGameStatus(status);
        }
      });
    }, 1 * 1000);
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  const value = useMemo(
    () =>
      gameStatus !== null
        ? new ConcreteGameInformation(gameId, username, gameStatus)
        : new BeforeReadyGameInformation(),

    [gameStatus, gameId, username]
  );

  return (
    <GameContext.Provider value={value}>{props.children}</GameContext.Provider>
  );
}
