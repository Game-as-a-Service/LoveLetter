import { GameContext } from "@/providers";
import { Seen } from "@/types";
import { Button } from "@chakra-ui/react";
import { useContext, useState } from "react";
import CopyToClipboard from "react-copy-to-clipboard";

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

export function GameStatusBoard() {
  const [copied, setCopied] = useState(false);
  const context = useContext(GameContext);
  if (!context.isReady()) {
    return <></>;
  }

  const gameStatus = context.getGameStatus();
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
      if (p.name === context.getUsername()) {
        seens = p.seen_cards;
      }
    });
  }

  if (context.isGameOver()) {
    gameProgress = "遊戲結束";
  }

  return (
    <>
      <div className="mb-5">
        <h1>遊戲狀態</h1>
        <div className="bg-gray-100 m-4 p-2 min-h-[3rem] pl-3 rounded-xl flex items-center border-2 border-red-700">
          {gameProgress}
        </div>
        <h1>玩家列表</h1>
        {data.map((x) => (
          <PlayerItem
            index={x.index}
            name={x.name}
            key={`PlayerItem_${x.index}`}
          ></PlayerItem>
        ))}
      </div>
      <div className="absolute top-2 left-2 border-2 border-black p-1 text-[10pt]">
        <div>玩家資訊</div>
        <div>
          gameId: {gameStatus?.game_id}
          <CopyToClipboard
            text={gameStatus?.game_id}
            onCopy={() => {
              setCopied(true);
            }}
          >
            <Button rounded="5px" size="xs" margin="5px" marginTop="0px">
              Copy
            </Button>
          </CopyToClipboard>
          {copied ? <span style={{ color: "red" }}>Copied.</span> : null}
        </div>
        <div>
          看到的牌：
          {seens.map((x, index) => (
            <SeenItem seen={x} key={`SeenItem_${x.card}`} />
          ))}
        </div>
      </div>
    </>
  );
}
