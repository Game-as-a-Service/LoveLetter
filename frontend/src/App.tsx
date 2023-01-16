import React, { useEffect, useState } from "react";
import "./App.css";
import { useGameId, useUsername } from "./hooks";
import { CreateOrJoinGame } from "./components/CreateOrJoinGame";
import { GameStatus, ViewState } from "./types";
import { GetGameStatus } from "./apis";

function GameRoom(props: { visitFunc: (view: ViewState) => void }) {
  const [username, setUsername] = useUsername();
  const [gameId, setGameId] = useGameId();

  useEffect(() => {}, [
    GetGameStatus(gameId, username).then((status: GameStatus) => {
      // TODO status 中沒有等待的玩家列表，需要改 api
      console.log(status);
    }),
  ]);

  return (
    <>
      <div>GameList: {username}</div>
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
