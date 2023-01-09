import React, { useState } from "react";
import "./App.css";
import { useUsername } from "./hooks";
import { CreateOrJoinGame } from "./components/CreateOrJoinGame";
import { ViewState } from "./types";

function GameList(props: { visitFunc: (view: ViewState) => void }) {
  const [username, setUsername] = useUsername();
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
      {flow === "game-list" && <GameList visitFunc={setFlow} />}
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
