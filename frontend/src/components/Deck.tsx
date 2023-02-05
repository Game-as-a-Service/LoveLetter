import React, { useContext } from "react";
import { CardAction } from "@/components/Cards";
import { GameContext } from "@/providers";
import { Flex } from "@chakra-ui/react";

export function Deck() {
  const context = useContext(GameContext);
  const width = 300;

  const empty = <Flex width={width}></Flex>;
  if (!context.IsReady()) {
    return empty;
  }

  if (!context.IsMyTurn()) {
    return empty;
  }

  const cards = context.GetTurnPlayer().cards;

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
            <CardAction handCard={cards[0]} key={0}/>
          </div>
          <div className="min-w-[15px]"></div>
          <div>
            <div className="text-xs">{cards[1].name}</div>
            <CardAction handCard={cards[1]} key={1}/>
          </div>
        </Flex>
      </Flex>
    </>
  );
}
