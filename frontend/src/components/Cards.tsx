import card_front from "./card-front.png";
import card_back from "./card-back.png";

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

export function CardFront() {
  return (
    <div className="w-[118px] h-[172px] shadow-xl shadow-zinc-500 container relative">
      <img src={card_front} className="bg-white rounded-xl" />
    </div>
  );
}
