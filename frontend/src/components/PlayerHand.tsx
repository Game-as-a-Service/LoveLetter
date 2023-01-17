import { CardBack, CardFront } from "./Cards";
import React from "react";
import { GameStatus } from "../types";

export function PlayerHand(props: {
  index: number;
  gameStatus: GameStatus | null;
}) {
  const { index, gameStatus } = props;

  if (gameStatus == null) {
    return <CardFront />;
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

  return (
    <div className="container relative">
      <CardBack enabled={true} />
      <div
        className="text-xs rounded-xl bg-amber-100 p-2 font-bold"
        style={{ position: "absolute", top: "-2.5rem", left: 5 }}
      >
        {playerName}
      </div>
    </div>
  );
}
