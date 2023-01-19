import { GameStatus, ViewState } from "../types";
import { useGameId, useUsername } from "../hooks";
import React, { useEffect, useState } from "react";
import { GetGameStatus, StartGame } from "../apis";
import { isEqual } from "lodash";
import { PlayerHand } from "./PlayerHand";
import { Deck } from "./Deck";
import { GameStatusBoard } from "./GameStatusBoard";
import { GameEvents } from "./GameEvents";
import { Box, Button } from "@chakra-ui/react";

function StartGameFunc(props: { gameStatus: GameStatus | null }) {
  const { gameStatus } = props;
  if (gameStatus == null) {
    return <></>;
  }
  if (gameStatus.players.length >= 2 && gameStatus.rounds.length == 0) {
    return (
      <Button
        colorScheme="twitter"
        onClick={() => {
          StartGame(gameStatus?.game_id).then((result) =>
            console.log(`${gameStatus?.game_id} started? => ${result}`)
          );
        }}
      >
        開始遊戲
      </Button>
    );
  }
  return <></>;
}

export function GameRoom(props: { visitFunc: (view: ViewState) => void }) {
  const [username] = useUsername();
  const [gameId] = useGameId();
  const [gameStatus, setGameStatus] = useState<GameStatus | null>(null);

  // refresh GameStatus every 1 seconds.
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
    }, 1 * 1000);
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  // TODO 需要有 "開始遊戲" 的功能

  return (
    <>
      <div className="flex h-screen bg-slate-200">
        <div className="w-[75vw] p-4 flex flex-col mx-auto">
          <div className="flex flex-grow items-center justify-center">
            <div className="flex h-[20vh]">
              <PlayerHand index={0} gameStatus={gameStatus} />
            </div>
          </div>
          <div className="flex min-h-[38vh] items-center justify-center">
            <div className="flex h-[20vh] m-4">
              <PlayerHand index={3} gameStatus={gameStatus} />
            </div>
            <div className="flex h-[20vh] w-[300px] m-4 ml-16 mr-16">
              <Deck></Deck>
            </div>
            <div className="flex h-[20vh] m-4">
              <PlayerHand index={1} gameStatus={gameStatus} />
            </div>
          </div>
          <div className="flex flex-grow items-center justify-center">
            <div className="flex h-[20vh]">
              <PlayerHand index={2} gameStatus={gameStatus} />
            </div>
          </div>
          <Box position="absolute" top={5} right="28vw">
            <StartGameFunc gameStatus={gameStatus} />
          </Box>
        </div>
        {/*<!-- Game Status-->*/}
        <div className="w-[25vw] p-4 border-l-2 border-slate-400 shadow-amber-300">
          <GameStatusBoard gameStatus={gameStatus} />
          {/* <!-- Game events --> */}
          <GameEvents events={gameStatus?.events} />
        </div>
      </div>
    </>
  );
}
