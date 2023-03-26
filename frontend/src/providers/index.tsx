import { useGameId, useUsername } from "@/hooks";
import { usePollGameStatus } from "@/hooks/usePollGameStatus";
import { GameStatus, TurnPlayer } from "@/types";
import { createContext, ReactNode, useMemo } from "react";

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
  constructor(username: string, gameStatus: GameStatus) {
    this.username = username;
    this.gameStatus = gameStatus;
  }

  getGameId(): string {
    return this.gameStatus.game_id;
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
    return this.gameStatus !== null;
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
      this.gameStatus.final_winner !== "" &&
      this.gameStatus.final_winner != null
    );
  }

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
  const gameStatus = usePollGameStatus(gameId, username);

  // Re-render only if the value of gameStatus and username got re-assigned.
  const value = useMemo(
    () =>
      gameStatus !== null
        ? new ConcreteGameInformation(username, gameStatus)
        : new BeforeReadyGameInformation(),
    [gameStatus, username]
  );

  return (
    <GameContext.Provider value={value}>{props.children}</GameContext.Provider>
  );
}
