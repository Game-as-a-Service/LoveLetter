// TODO 也許需要整理一下卡牌效果的事件
export interface TriggerBy {
  trigger_by: string;
  card?: string;
  out?: string;
  who?: string;
  protected?: string;
}

export interface TookEffect {
  event?: TriggerBy;
  took: boolean;
}

export interface CardEvent {
  type: "card_action";
  card: string;
  to?: string;
  with_card?: string;
  turn_player: string;
  took_effect: TookEffect;
}

export interface RoundEvent {
  type: "round_started";
  winner?: string;
}

export interface GameOverEvent {
  type: "game_over";
  final_winner?: string;
}

export type GameEvent = CardEvent | RoundEvent | GameOverEvent;
