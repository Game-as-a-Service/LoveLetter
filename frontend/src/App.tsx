import React, { useState } from "react";
import "./App.css";

import { CreateOrJoinGame, GameRoom } from "@/components";
import { ViewState } from "@/types";

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
