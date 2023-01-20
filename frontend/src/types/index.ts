import exp from "constants";

export type ViewState = "pick-name" | "game-list" | "game-room";

export interface NamedPlayer {
  name: string;
  score: number;
}

export interface SeenCard {
  name: string;
}

export interface Seen {
  opponent_name: string;
  card: SeenCard;
}

export interface RoundPlayer {
  name: string;
  seen_cards: Array<Seen>;
  cards: Array<HandCard>;
}

export interface TurnPlayer {
  name: string;
  out: boolean;
  cards: Array<HandCard>;
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

export interface RoundEvent {
  type: "round_started";
  winner?: string;
}

export type GameEvent = CardEvent | RoundEvent;

export interface GameStatus {
  game_id: string;
  players: Array<NamedPlayer>;
  rounds: Array<Round>;
  events: Array<GameEvent>;
}
