import React, { useEffect, useState } from "react";
import "./App.css";
import { useGameId, useUsername } from "./hooks";
import { CreateOrJoinGame } from "./components/CreateOrJoinGame";
import { GameStatus, ViewState } from "./types";
import { GetGameStatus } from "./apis";
import { isEqual } from "lodash";
import { CardBack, CardFront } from "./components/Cards";
import { Deck } from "./components/Deck";
import { PlayerList } from "./components/PlayerList";
import { GameEvents } from "./components/GameEvents";

function PlayerHand() {
  return (
    <>
      {/*<div className="w-[118px] h-[172px] shadow-xl shadow-zinc-500 container relative">*/}
      {/*  <img src="card-front.svg" alt="" className="bg-white rounded-xl">*/}

      {/*    <div className="flex flex-col absolute top-[15px] p-2 text-white items-center">*/}
      {/*      <div className="text-xs mb-1">8</div>*/}
      {/*      <div className="text-2xl">公主</div>*/}
      {/*      <div className="text-[8pt] mt-2 p-1">*/}
      {/*        當你丟棄公主時，你立即出局。*/}
      {/*      </div>*/}
      {/*    </div>*/}

      {/*</div>*/}
      {/*<CardBack />*/}
      <CardBack />
      <CardFront />
    </>
  );
}

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

  return (
    <>
      {/*<div className="flex h-screen bg-slate-200">*/}

      {/*  <div>GameList: {username}</div>*/}
      {/*  <div>{JSON.stringify(gameStatus)}</div>*/}
      {/*</div>*/}
      <div className="flex h-screen bg-slate-200">
        <div className="w-[75vw] p-4 flex flex-col mx-auto">
          <div className="flex flex-grow items-center justify-center">
            <div className="flex h-[20vh]">
              <PlayerHand />
            </div>
          </div>
          <div className="flex min-h-[38vh] items-center justify-center">
            <div className="flex h-[20vh] m-4">
              <PlayerHand />
            </div>
            <div className="flex h-[20vh] w-[300px] m-4 ml-16 mr-16">
              <Deck></Deck>
            </div>
            <div className="flex h-[20vh] m-4">
              <PlayerHand />
            </div>
          </div>
          <div className="flex flex-grow items-center justify-center">
            <div className="flex h-[20vh]">
              <PlayerHand />
            </div>
          </div>
        </div>
        {/*<!-- Game Status-->*/}
        <div className="w-[25vw] p-4 border-l-2 border-slate-400 shadow-amber-300">
          <PlayerList />
          {/* <!-- Game events --> */}
          <GameEvents />
        </div>
      </div>
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
