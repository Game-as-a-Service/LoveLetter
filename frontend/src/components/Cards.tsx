import card_front from "./card-front.png";
import card_back from "./card-back.png";

export function CardBack() {
  return (
    <div className="w-[118px] h-[172px] shadow-xl shadow-zinc-500 container relative">
      <img src={card_back} className="bg-white rounded-xl" />
    </div>
  );
}

export function CardFront() {
  return (
    <div className="w-[118px] h-[172px] shadow-xl shadow-zinc-500 container relative">
      <img src={card_front} className="bg-white rounded-xl" />
    </div>
  );
}
