import exp from "constants";

export type ViewState = "pick-name" | "game-list" | "game-room";

export interface NamedPlayer {
  name: string;
}

export interface RoundPlayer {
  name: string;
}

export interface HandCard {
  name: string;
  description: string;
  value: number;
}

export interface TurnPlayer {
  name: string;
  out: boolean;
  cards: Array<HandCard>;
}

export interface Round {
  turn_player: TurnPlayer;
  players: Array<RoundPlayer>;
}

export interface GameStatus {
  game_id: string;
  players: Array<NamedPlayer>;
  rounds: Array<Round>;
}
