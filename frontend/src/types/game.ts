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
  start_player: string;
}
