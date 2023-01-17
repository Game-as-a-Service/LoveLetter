import React, { useState } from "react";
import "./App.css";
import { CreateOrJoinGame } from "./components/CreateOrJoinGame";
import { ViewState } from "./types";
import { GameRoom } from "./components/GameRoom";

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
