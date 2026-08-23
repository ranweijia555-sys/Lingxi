"use client";

import { useLanguage } from "@/lib/language";

export type ReadingMode = "draw" | "photo";

interface ModeToggleProps {
  mode: ReadingMode;
  onChange: (mode: ReadingMode) => void;
}

export default function ModeToggle({ mode, onChange }: ModeToggleProps) {
  const { language } = useLanguage();

  return (
    <div className="mode-toggle" aria-label="选择抽牌方式">
      <button
        type="button"
        className={mode === "draw" ? "active" : ""}
        onClick={() => onChange("draw")}
      >
        <span className="mode-number">01</span>
        <span>
          <strong>{language === "zh" ? "线上抽牌" : "Draw online"}</strong>
          <small>{language === "zh" ? "从完整牌阵中凭直觉选择" : "Choose intuitively from the full deck"}</small>
        </span>
      </button>
      <button
        type="button"
        className={mode === "photo" ? "active" : ""}
        onClick={() => onChange("photo")}
      >
        <span className="mode-number">02</span>
        <span>
          <strong>{language === "zh" ? "识别实体牌" : "Scan physical cards"}</strong>
          <small>{language === "zh" ? "上传你已经抽好的牌面照片" : "Upload a photo of cards you have drawn"}</small>
        </span>
      </button>
    </div>
  );
}
