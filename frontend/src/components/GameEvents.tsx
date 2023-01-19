import React from "react";
import { CardEvent } from "../types";
import { Badge } from "@chakra-ui/react";
import new_icon from "./icons8-new-60.png";

function NewIcon(props: { display: boolean }) {
  // source: https://icons8.com/icons/set/new
  if (!props.display) {
    return <></>;
  }
  return (
    <img
      src={new_icon}
      alt=""
      width={24}
      className="ml-2 shadow-2xl shadow-amber-500"
    />
  );
}

function EventView(props: { event: CardEvent; index: number }) {
  const { event, index } = props;

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
        <NewIcon display={index === 0} />
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
        <NewIcon display={index === 0} />
      </div>
    );
  }

  return (
    <div className="m-1 p-2 min-h-[1rem] pl-3 rounded-xl flex items-center text-[12px]">
      <Badge colorScheme="blue">{event.turn_player}</Badge>
      &nbsp;使用&nbsp;
      <Badge colorScheme="purple">{event.card}</Badge>
      <NewIcon display={index === 0} />
    </div>
  );
}

function lastN(n: number, events: Array<CardEvent>): Array<CardEvent> {
  if (events === undefined) {
    return [];
  }
  const elems = events.slice(-n);
  elems.reverse();
  return elems;
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
    <div className="flex-auto">
      <h1>遊戲事件</h1>
      <div className="overflow-y-auto border-2 border-black shadow-2xl">
        {lastN(8, events as Array<CardEvent>).map((evt, index) => (
          <EventView event={evt} index={index} />
        ))}
      </div>
    </div>
  );
}
