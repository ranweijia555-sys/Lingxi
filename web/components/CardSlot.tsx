"use client";

import Image from "next/image";

import { CARD_BACK_PATH, cardImagePath } from "@/lib/card-images";
import { useLanguage } from "@/lib/language";
import type { CardDisplay, Orientation } from "@/lib/types";

interface CardSlotProps {
  index: number;
  label: string;
  card?: { orientation: Orientation; display: CardDisplay };
  isCore?: boolean;
  revealed: boolean;
}

export default function CardSlot({ index, label, card, isCore, revealed }: CardSlotProps) {
  const { language } = useLanguage();
  const cardName = card ? (language === "zh" ? card.display.name_zh : card.display.name_en) : "";
  const orientation = card?.orientation === "upright"
    ? language === "zh" ? "正位" : "Upright"
    : language === "zh" ? "逆位" : "Reversed";

  return (
    <div className={`slot ${card ? "filled" : ""}`} style={{ animationDelay: `${index * 0.12}s` }}>
      <div className="slot-frame" data-i={index + 1}>
        {card && (
          <div className="flip">
            <div
              className={`flip-inner ${revealed ? "revealed" : ""}`}
              style={{ transitionDelay: revealed ? `${index * 260}ms` : "0ms" }}
            >
              <div className="face front cardback">
                <Image src={CARD_BACK_PATH} alt={language === "zh" ? "塔罗牌背" : "Tarot card back"} fill sizes="(max-width: 640px) 96px, 150px" />
              </div>
              <div className={`face back cardface ${isCore ? "core" : ""}`}>
                <Image
                  className={card.orientation === "reversed" ? "tarot-image reversed" : "tarot-image"}
                  src={cardImagePath(card.display.name_zh)}
                  alt={`${cardName}, ${orientation}`}
                  fill
                  sizes="(max-width: 640px) 96px, 150px"
                />
                {isCore && <div className="core-badge">{language === "zh" ? "核心牌" : "Core"}</div>}
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="slot-caption">
        <span className="slot-label">{label}</span>
        {revealed && card && (
          <span className="slot-card-name">
            {cardName} · {orientation}
          </span>
        )}
      </div>
    </div>
  );
}
