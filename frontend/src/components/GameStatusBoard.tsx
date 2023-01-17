import React from "react";
import { GameStatus } from "../types";

function PlayerItem(props: { index: number; name: string }) {
  if (props.name === "-") {
    return (
      <div className="bg-gray-400 m-4 p-2 min-h-[3rem] pl-3 rounded-xl flex items-center">
        玩家{props.index}：-
      </div>
    );
  }

  return (
    <div className="bg-amber-200 m-4 p-2 min-h-[3rem] pl-3 rounded-xl flex items-center">
      玩家{props.index}：{props.name}
    </div>
  );
}

export function GameStatusBoard(props: { gameStatus: GameStatus | null }) {
  const { gameStatus } = props;
  let gameProgress = "...(未知)...";

  const data = [
    { name: "-", index: 1 },
    { name: "-", index: 2 },
    { name: "-", index: 3 },
    { name: "-", index: 4 },
  ];

  // game has not stared, use the top player list
  if (gameStatus != null && gameStatus.rounds.length === 0) {
    gameProgress = "等待玩家加入中...";
    if (gameStatus.players.length >= 2) {
      gameProgress = "等待遊戲開始...";
    }

    gameStatus.players.map((p, idx) => {
      data[idx] = { name: p.name, index: idx + 1 };
    });
  }

  // TODO

  return (
    <>
      <div className="mb-5">
        <h1>遊戲狀態</h1>
        <div className="bg-gray-100 m-4 p-2 min-h-[3rem] pl-3 rounded-xl flex items-center">
          {gameProgress}
        </div>
        <h1>玩家列表</h1>
        {data.map((x) => (
          <PlayerItem index={x.index} name={x.name}></PlayerItem>
        ))}
      </div>
    </>
  );
}
