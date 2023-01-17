import {CardBack, CardFront} from "./Cards";
import React from "react";

export function PlayerHand() {
    return (
        <>
            {/*<div className="w-[118px] h-[172px] shadow-xl shadow-zinc-500 container relative">*/}
            {/*  <img src="card-front.svg" alt="" className="bg-white rounded-xl">*/}

            {/*    <div className="flex flex-col absolute top-[15px] p-2 text-white items-center">*/}
            {/*      <div className="text-xs mb-1">8</div>*/}
            {/*      <div className="text-2xl">公主</div>*/}
            {/*      <div className="text-[8pt] mt-2 p-1">*/}
            {/*        當你丟棄公主時，你立即出局。*/}
            {/*      </div>*/}
            {/*    </div>*/}

            {/*</div>*/}
            {/*<CardBack />*/}
            <CardBack/>
            <CardFront/>
        </>
    );
}
