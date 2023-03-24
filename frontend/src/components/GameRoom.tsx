import React, { useContext } from "react";
import { Box, Button } from "@chakra-ui/react";
import { GameStatus, ViewState } from "@/types";
import { StartGame } from "@/apis";
import { GameStatusBoard } from "@/components/GameStatusBoard";
import { GameEvents } from "@/components/GameEvents";
import { PlayerHand } from "@/components/PlayerHand";
import { Deck } from "@/components/Deck";
import { GameContext } from "@/providers";

function StartGameFunc(props: { gameStatus: GameStatus | null }) {
  const { gameStatus } = props;
  if (gameStatus == null) {
    return <></>;
  }
  if (gameStatus.players.length >= 2 && gameStatus.rounds.length === 0) {
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
  const context = useContext(GameContext);
  if (!context.isReady()) {
    return <></>;
  }

  const gameStatus = context.getGameStatus();

  return (
    <>
      <div className="flex h-screen bg-slate-200">
        <div className="w-[75vw] p-4 flex flex-col mx-auto">
          <div className="flex flex-grow items-center justify-center">
            <div className="flex h-[20vh]">
              <PlayerHand index={0} />
            </div>
          </div>
          <div className="flex min-h-[38vh] items-center justify-center">
            <div className="flex h-[20vh] m-4">
              <PlayerHand index={3} />
            </div>

            <div className="flex h-[20vh] w-[350px] m-4 ml-16 mr-16 flex-row">
              <Deck />
            </div>
            <div className="flex h-[20vh] m-4">
              <PlayerHand index={1} />
            </div>
          </div>
          <div className="flex flex-grow items-center justify-center">
            <div className="flex h-[20vh]">
              <PlayerHand index={2} />
            </div>
          </div>
          <Box position="absolute" top={5} right="28vw">
            <StartGameFunc gameStatus={gameStatus} />
          </Box>
        </div>
        {/*<!-- Game Status-->*/}
        <div className="w-[25vw] p-4 border-l-2 border-slate-400 shadow-amber-300 max-h-[100vh]">
          <GameStatusBoard />
          {/* <!-- Game events --> */}
          <GameEvents />
        </div>
      </div>
    </>
  );
}
