import { CardBack, CardFront } from "./Cards";
import React from "react";
import { GameStatus, HandCard } from "../types";
import { useUsername } from "../hooks";

export function PlayerHand(props: {
  index: number;
  gameStatus: GameStatus | null;
}) {
  const [username] = useUsername();
  const { index, gameStatus } = props;

  if (gameStatus == null) {
    return <CardBack enabled={false} />;
  }

  if (gameStatus.players[index] === undefined) {
    return (
      <div>
        <CardBack enabled={false} />
      </div>
    );
  }

  let playerName = "";
  // TODO turn player should show two cards
  if (gameStatus.rounds.length == 0) {
    playerName = gameStatus.players[index].name;
  } else {
    // TODO use the rounds data
    playerName = gameStatus.players[index].name;
  }

  const is_current_user = playerName === username;
  const current_round = gameStatus.rounds[gameStatus.rounds.length - 1];
  let is_turn_player = false;
  if (current_round) {
    is_turn_player = playerName === current_round.turn_player.name;
  }

  let hand_cards: Array<HandCard> = [];
  if (is_turn_player && is_current_user) {
    hand_cards = current_round.turn_player.cards;
  } else if (is_current_user) {
    current_round?.players?.forEach((r) => {
      if (r.name == playerName) {
        hand_cards = r.cards;
      }
    });
  }

  return (
    <div className="container relative">
      <div>
        {!is_turn_player && !is_current_user && <CardBack enabled={true} />}
        {!is_turn_player && is_current_user && (
          <CardFront handCard={hand_cards[0]} />
        )}
        {is_turn_player && is_current_user && (
          <div className="flex">
            {hand_cards.map((x) => (
              <CardFront
                key={`${x.name}${playerName}`}
                handCard={x}
              ></CardFront>
            ))}
          </div>
        )}
        {is_turn_player && !is_current_user && (
          <div className="flex border-8 border-lime-400 rounded-xl">
            <CardBack enabled={true}></CardBack>
            <CardBack enabled={true}></CardBack>
          </div>
        )}
      </div>

      <div
        className={`text-xs rounded-xl bg-amber-100 p-2 font-bold ${
          is_current_user ? "border-2 border-amber-500" : ""
        }`}
        style={{ position: "absolute", top: "-2.5rem", left: 5 }}
      >
        {playerName}
      </div>
    </div>
  );
}
