import React from "react";
import { CardEvent, GameEvent } from "../types";
import { Badge, Box } from "@chakra-ui/react";
import new_icon from "./icons8-new-60.png";
import { CardBack } from "./Cards";
import { divide } from "lodash";

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

function RoundEventView(props: { event: GameEvent; index: number }) {
  const { event, index } = props;

  if (event.type !== "round_started") {
    return <></>;
  }

  return (
    <div className="m-1 p-2 min-h-[1rem] pl-3 rounded-xl flex items-center text-[12px]">
      <Badge variant="solid" colorScheme="green">
        round started
      </Badge>
      {event.winner && (
        <>
          <Badge variant="solid" colorScheme="messenger" ml={2}>
            {event.winner}
          </Badge>
          <Box ml={2}>成功送信給公主</Box>
        </>
      )}
    </div>
  );
}

function CardEventView(props: { event: GameEvent; index: number }) {
  const { event, index } = props;

  if (event.type !== "card_action") {
    return <></>;
  }

  let extra: JSX.Element = <></>;
  if (event.took_effect.event !== null) {
    const evt = event.took_effect.event;
    if (evt?.out) {
      extra = (
        <div className="m-1 p-2 min-h-[1rem] pl-3 rounded-xl flex items-center text-[12px] bg-slate-300">
          <div className="font-extrabold mr-2">{evt.out}</div>
          出局
        </div>
      );
    } else if (evt?.who) {
      extra = (
        <div className="m-1 p-2 min-h-[1rem] pl-3 rounded-xl flex items-center text-[12px] bg-slate-300">
          <div className="font-extrabold mr-2">{evt.who}</div>
          <div className="mr-2">丟棄</div>
          <div className="font-extrabold">{evt.card}</div>
        </div>
      );
    } else if (evt?.protected) {
      extra = (
        <div className="m-1 p-2 min-h-[1rem] pl-3 rounded-xl flex items-center text-[12px] bg-slate-300">
          <div className="font-extrabold mr-2">{evt.protected}</div>
          <div className="mr-2">被侍女保護中</div>
          <div className="font-extrabold mr-2">{evt.trigger_by}</div>
          <div className="mr-2">無效</div>
        </div>
      );
    } else {
      extra = (
        <div>
          {"wip::"}
          {JSON.stringify(evt)}
        </div>
      );
    }
  }

  return (
    <>
      {extra}
      <CardActionItem {...props} />
    </>
  );
}

function CardActionItem(props: { event: GameEvent; index: number }) {
  const { event, index } = props;
  if (event.type !== "card_action") {
    return <></>;
  }
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

function lastN(n: number, events: Array<GameEvent>): Array<GameEvent> {
  if (events === undefined) {
    return [];
  }
  const elems = events.slice(-n);
  elems.reverse();
  return elems;
}

export function GameEvents(props: { events?: Array<GameEvent> }) {
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
        {lastN(8, events as Array<GameEvent>).map((evt, index) => (
          <>
            <RoundEventView event={evt} index={index} />
            <CardEventView event={evt} index={index} />
          </>
        ))}
      </div>
    </div>
  );
}
