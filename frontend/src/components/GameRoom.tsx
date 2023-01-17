import { GameStatus, ViewState } from "../types";
import { useGameId, useUsername } from "../hooks";
import React, { useEffect, useState } from "react";
import { GetGameStatus } from "../apis";
import { isEqual } from "lodash";
import { PlayerHand } from "./PlayerHand";
import { Deck } from "./Deck";
import { GameStatusBoard } from "./GameStatusBoard";
import { GameEvents } from "./GameEvents";

export function GameRoom(props: { visitFunc: (view: ViewState) => void }) {
  const [username] = useUsername();
  const [gameId] = useGameId();
  const [gameStatus, setGameStatus] = useState<GameStatus | null>(null);

  // refresh GameStatus every 5 seconds.
  useEffect(() => {
    // set GameStatus before the refresher triggered
    GetGameStatus(gameId, username).then((status: GameStatus) => {
      if (!isEqual(gameStatus, status)) {
        setGameStatus(status);
      }
    });

    const intervalId = setInterval(() => {
      // auto-refresh GameStatus
      GetGameStatus(gameId, username).then((status: GameStatus) => {
        if (!isEqual(gameStatus, status)) {
          setGameStatus(status);
        }
      });
    }, 5 * 1000);
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  // TODO 需要有 "開始遊戲" 的功能

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
          <GameStatusBoard gameStatus={gameStatus} />
          {/* <!-- Game events --> */}
          <GameEvents />
        </div>
      </div>
    </>
  );
}
