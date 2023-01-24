import React, { useState } from "react";
import "./App.css";

import { CreateOrJoinGame, GameRoom } from "@/components";
import { ViewState } from "@/types";
import { GameDataProvider } from "@/providers";

function GameUI() {
  const [flow, setFlow] = useState<ViewState>("pick-name");

  return (
    <>
      {flow === "pick-name" && <CreateOrJoinGame visitFunc={setFlow} />}
      {flow === "game-room" && (
        <GameDataProvider>
          <GameRoom visitFunc={setFlow} />
        </GameDataProvider>
      )}
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
