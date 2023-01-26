import card_front from "./card-front.png";
import card_back from "./card-back.png";

import { Button, Select } from "@chakra-ui/react";
import { useRef } from "react";

import { useGameId, useUsername } from "@/hooks";
import { HandCard } from "@/types";
import { PlayCard } from "@/apis";

export function CardBack(props: { enabled: boolean }) {
  let cssConfig = {};
  if (props.enabled === false) {
    cssConfig = { filter: "grayscale(1)", opacity: 0.7 };
  }
  return (
    <div className="w-[118px] h-[172px] shadow-xl shadow-zinc-500 container relative">
      <img
        alt=""
        src={card_back}
        className="bg-white rounded-xl gr"
        style={cssConfig}
      />
    </div>
  );
}

export function CardAction(props: { handCard: HandCard }) {
  const [gameId] = useGameId();
  const [username] = useUsername();
  const { handCard } = props;
  const ref_chosen_player = useRef(null);
  const ref_guessed_card = useRef(null);

  if (!handCard.usage.can_discard) {
    return <></>;
  }

  const has_player_options = handCard.usage.choose_players.length > 0;
  const has_guess_card_options = handCard.usage.can_guess_cards.length > 0;

  return (
    <>
      {has_player_options && (
        <Select
          size="xs"
          defaultValue={handCard.usage.choose_players[0]}
          ref={ref_chosen_player}
          onChange={(e) => {
            console.log(e.target.value);
          }}
        >
          {handCard.usage.choose_players.map((x) => (
            <option value={x}>{x}</option>
          ))}
        </Select>
      )}
      {has_guess_card_options && (
        <Select
          size="xs"
          defaultValue={handCard.usage.can_guess_cards[0]}
          ref={ref_guessed_card}
          onChange={(e) => {
            console.log(e.target.value);
          }}
        >
          {handCard.usage.can_guess_cards.map((x) => (
            <option value={x}>{x}</option>
          ))}
        </Select>
      )}
      <Button
        size="xs"
        onClick={() => {
          const payload: { [prop: string]: string } = {};
          if (ref_chosen_player.current) {
            payload.chosen_player = (
              ref_chosen_player.current as HTMLSelectElement
            ).value;
          }
          if (ref_guessed_card.current) {
            payload.guess_card = (
              ref_guessed_card.current as HTMLSelectElement
            ).value;
          }

          PlayCard(gameId, username, handCard.name, payload);
        }}
      >
        出牌
      </Button>
    </>
  );
}

export function CardFront(props: { handCard: HandCard }) {
  const { handCard } = props;

  if (handCard === undefined) {
    return <CardBack enabled={true} />;
  }

  return (
    <div className="w-[118px] h-[172px] shadow-xl shadow-zinc-500 container relative">
      <img src={card_front} className="bg-white rounded-xl" />
      <div className="flex flex-col absolute top-[15px] p-2 text-white items-center">
        <div className="text-xs mb-1">{handCard.value}</div>
        <div className="text-2xl">{handCard.name}</div>
        <div className="text-[8pt] mt-2 p-1">{handCard.description}</div>
      </div>
      <div>{/*<CardAction handCard={handCard} />*/}</div>
    </div>
  );
}
