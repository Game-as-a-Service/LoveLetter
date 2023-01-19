import React from "react";
import { GameStatus, Seen } from "../types";
import { useGameId, useUsername } from "../hooks";
import exp from "constants";

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

export function SeenItem(props: { seen: Seen }) {
  const { seen } = props;
  return (
    <>
      <div className="text-gray-600">
        看到 {seen.opponent_name} 持有 {seen.card.name}
      </div>
    </>
  );
}

export function GameStatusBoard(props: { gameStatus: GameStatus | null }) {
  const { gameStatus } = props;
  const [username] = useUsername();
  let gameProgress = "...(未知)...";

  const data = [
    { name: "-", index: 1 },
    { name: "-", index: 2 },
    { name: "-", index: 3 },
    { name: "-", index: 4 },
  ];

  if (gameStatus != null) {
    gameStatus.players.map((p, idx) => {
      data[idx] = { name: p.name, index: idx + 1 };
    });
  }

  // game has not stared, use the top player list
  if (gameStatus != null && gameStatus.rounds.length === 0) {
    gameProgress = "等待玩家加入中...";
    if (gameStatus.players.length >= 2) {
      gameProgress = "等待遊戲開始...";
    }
  }

  let seens: Array<Seen> = [];

  // the game has started
  if (gameStatus != null && gameStatus.rounds.length > 0) {
    const current_round = gameStatus.rounds[gameStatus.rounds.length - 1];
    gameProgress = `等待 ${current_round.turn_player.name} 出牌...`;

    current_round.players.map((p) => {
      if (p.name === username) {
        seens = p.seen_cards;
      }
    });
  }

  // TODO 如果可以知道遊戲結束的狀態時，要能顯示遊戲結束的贏家

  return (
    <>
      <div className="mb-5">
        <h1>遊戲狀態</h1>
        <div className="bg-gray-100 m-4 p-2 min-h-[3rem] pl-3 rounded-xl flex items-center border-2 border-red-700">
          {gameProgress}
        </div>
        <h1>玩家列表</h1>
        {data.map((x) => (
          <PlayerItem index={x.index} name={x.name}></PlayerItem>
        ))}
      </div>
      <div className="absolute top-2 left-2 border-2 border-black p-1 text-[10pt]">
        <div>玩家資訊</div>
        <div>gameId: {gameStatus?.game_id}</div>
        <div>
          看到的牌：
          {seens.map((x) => (
            <SeenItem seen={x} />
          ))}
        </div>
      </div>
    </>
  );
}
