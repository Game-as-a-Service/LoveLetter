import React, { useContext } from "react";
import { CardAction } from "@/components/Cards";
import { GameContext } from "@/providers";
import { Flex } from "@chakra-ui/react";

export function Deck() {
  const context = useContext(GameContext);
  const width = 300;

  const empty = <Flex width={width}></Flex>;
  if (!context.isReady()) {
    return empty;
  }

  if (context.isGameOver()) {
    return empty;
  }

  if (!context.isMyTurn()) {
    return empty;
  }

  const cards = context.getTurnPlayer().cards;

  return (
    <>
      <Flex
        bg="gray.300"
        width={width}
        justifyContent="center"
        alignItems="center"
        rounded={5}
      >
        <Flex>
          <div>
            <div className="text-xs">{cards[0].name}</div>
            <CardAction handCard={cards[0]} />
          </div>
          <div className="min-w-[15px]"></div>
          <div>
            <div className="text-xs">{cards[1].name}</div>
            <CardAction handCard={cards[1]} />
          </div>
        </Flex>
      </Flex>
    </>
  );
}
