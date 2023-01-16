import React, { useEffect, useState } from "react";
import "./App.css";
import { useGameId, useUsername } from "./hooks";
import { CreateOrJoinGame } from "./components/CreateOrJoinGame";
import { GameStatus, ViewState } from "./types";
import { GetGameStatus } from "./apis";
import { isEqual } from "lodash";

function GameRoom(props: { visitFunc: (view: ViewState) => void }) {
  const [username] = useUsername();
  const [gameId] = useGameId();
  const [gameStatus, setGameStatus] = useState<GameStatus | null>();

  // TODO 自動 refresh game status
  // TODO 需要有 "開始遊戲" 的功能
  useEffect(() => {}, [
    GetGameStatus(gameId, username).then((status: GameStatus) => {
      // TODO status 中沒有等待的玩家列表，需要改 api
      console.log(status);
      console.log(status.players[0].name);
      if (!isEqual(gameStatus, status)) {
        setGameStatus(status);
      }
    }),
  ]);

  // TODO 把 demo-sample 的圖搬進來
  return (
    <>
      <div>GameList: {username}</div>
      <div>{JSON.stringify(gameStatus)}</div>
    </>
  );
}

function GameUI() {
  const [flow, setFlow] = useState<ViewState>("pick-name");

  return (
    <>
      {flow === "pick-name" && <CreateOrJoinGame visitFunc={setFlow} />}
      {flow === "game-room" && <GameRoom visitFunc={setFlow} />}
    </>
  );
}

function App() {
  return (
    <>
      <GameUI />
    </>
  );
}

export default App;
