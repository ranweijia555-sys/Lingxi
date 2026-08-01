import type { CardDisplay, Orientation } from "@/lib/types";

interface CardSlotProps {
  index: number;
  label: string;
  card?: { orientation: Orientation; display: CardDisplay };
  isCore?: boolean;
  revealed: boolean;
}

export default function CardSlot({ index, label, card, isCore, revealed }: CardSlotProps) {
  return (
    <div className={`slot ${card ? "filled" : ""}`}>
      <div className="slot-frame" data-i={index + 1}>
        {card && (
          <div className="flip">
            <div
              className={`flip-inner ${revealed ? "revealed" : ""}`}
              style={{ transitionDelay: revealed ? `${index * 260}ms` : "0ms" }}
            >
              <div className="face front cardback">
                <div className="ring" />
                <div className="sigil">✦</div>
              </div>
              <div className={`face back cardface ${isCore ? "core" : ""}`}>
                <div className="rn">{card.orientation === "upright" ? "正位 ⬆" : "逆位 ⬇"}</div>
                <div className="glyph">{isCore ? "⊹" : "✦"}</div>
                <div>
                  <div className="nm">{card.display.name_zh}</div>
                  <div className="en">{card.display.name_en}</div>
                </div>
                <div className="kw">{card.display.keyword}</div>
                {isCore && <div className="core-badge">⊹ 核心牌 ⊹</div>}
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="slot-label">{label}</div>
    </div>
  );
}
