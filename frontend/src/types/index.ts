export type ViewState = "pick-name" | "game-list" | "game-room";

export interface GameStatus {
  game_id: string;
  rounds: [];
}
