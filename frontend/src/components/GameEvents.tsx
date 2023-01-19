import React from "react";
import { CardEvent } from "../types";
import { Badge } from "@chakra-ui/react";

function EventView(props: { event: CardEvent }) {
  const { event } = props;
  if (event.with_card != null) {
    return (
      <div className="m-1 p-2 min-h-[1rem] pl-3 rounded-xl flex items-center text-[12px]">
        <Badge colorScheme="blue">{event.turn_player}</Badge>
        &nbsp;使用&nbsp;
        <Badge colorScheme="purple">{event.card}</Badge>
        &nbsp;猜測&nbsp;
        <Badge colorScheme="red">{event.to}</Badge>
        &nbsp;有&nbsp;
        <Badge colorScheme="purple">{event.with_card}</Badge>
      </div>
    );
  }

  if (event.to != null) {
    return (
      <div className="m-1 p-2 min-h-[1rem] pl-3 rounded-xl flex items-center text-[12px]">
        <Badge colorScheme="blue">{event.turn_player}</Badge>
        &nbsp;對&nbsp;
        <Badge colorScheme="red">{event.to}</Badge>
        &nbsp;使用&nbsp;
        <Badge colorScheme="purple">{event.card}</Badge>
      </div>
    );
  }

  return (
    <div className="m-1 p-2 min-h-[1rem] pl-3 rounded-xl flex items-center text-[12px]">
      <Badge colorScheme="blue">{event.turn_player}</Badge>
      &nbsp;使用&nbsp;
      <Badge colorScheme="purple">{event.card}</Badge>
    </div>
  );
}

export function GameEvents(props: { events?: Array<CardEvent> }) {
  const { events } = props;
  if (events === null || events?.length === 0) {
    return (
      <div>
        <h1>遊戲事件</h1>
        <div className="bg-blue-200 m-4 p-2 min-h-[3rem] pl-3 rounded-xl flex items-center">
          - (沒有消息) -
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1>遊戲事件</h1>
      {events?.map((evt) => (
        <EventView event={evt} />
      ))}
    </div>
  );
}
