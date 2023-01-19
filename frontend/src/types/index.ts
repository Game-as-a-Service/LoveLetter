import exp from "constants";

export type ViewState = "pick-name" | "game-list" | "game-room";

export interface NamedPlayer {
  name: string;
}

export interface RoundPlayer {
  name: string;
}

export interface CardUsage {
  can_discard: true;
  choose_players: Array<string>;
  can_guess_cards: Array<string>;
}

export interface HandCard {
  name: string;
  description: string;
  value: number;
  usage: CardUsage;
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

export interface CardEvent {
  type: "card_action";
  card: string;
  to?: string;
  with_card?: string;
  turn_player: string;
}

export interface GameStatus {
  game_id: string;
  players: Array<NamedPlayer>;
  rounds: Array<Round>;
  events: Array<CardEvent>;
}
