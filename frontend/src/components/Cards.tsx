import card_front from "./card-front.png";
import card_back from "./card-back.png";
import { HandCard } from "../types";

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

export function CardFront(props: { handCard: HandCard }) {
  const { handCard } = props;
  return (
    <div className="w-[118px] h-[172px] shadow-xl shadow-zinc-500 container relative">
      <img src={card_front} className="bg-white rounded-xl" />
      <div className="flex flex-col absolute top-[15px] p-2 text-white items-center">
        <div className="text-xs mb-1">{handCard.value}</div>
        <div className="text-2xl">{handCard.name}</div>
        <div className="text-[8pt] mt-2 p-1">{handCard.description}</div>
      </div>
    </div>
  );
}
