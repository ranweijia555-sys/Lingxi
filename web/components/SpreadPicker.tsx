"use client";

import type { ReactNode } from "react";

import { localizedSpread, useLanguage } from "@/lib/language";
import type { Spread } from "@/lib/types";

interface SpreadPickerProps {
  spreads: Spread[];
  spreadKey: string;
  onSpreadChange: (key: string) => void;
  question: string;
  onQuestionChange: (q: string) => void;
  onStart: () => void;
  showStartButton?: boolean;
  children?: ReactNode;
}

export default function SpreadPicker({
  spreads,
  spreadKey,
  onSpreadChange,
  question,
  onQuestionChange,
  onStart,
  showStartButton = true,
  children,
}: SpreadPickerProps) {
  const selected = spreads.find((s) => s.key === spreadKey);
  const { language } = useLanguage();
  const selectedCopy = selected ? localizedSpread(selected, language) : undefined;

  return (
    <div className="setup-panel">
      <div className="panel-heading">
        <span className="eyebrow">READING SETUP</span>
        <h2>{language === "zh" ? "定义你的问题" : "Frame your question"}</h2>
        <p>{language === "zh" ? "清晰的问题，会让牌面给出更具体的回应。" : "A clear question gives the cards a more useful focus."}</p>
      </div>
      <label className="field-label" htmlFor="spread-select">
        <span>01</span> {language === "zh" ? "选择牌阵" : "Choose a spread"}
      </label>
      <select id="spread-select" value={spreadKey} onChange={(e) => onSpreadChange(e.target.value)}>
        {!spreads.length && <option value="">{language === "zh" ? "正在读取牌阵…" : "Loading spreads…"}</option>}
        {spreads.map((s) => (
          <option key={s.key} value={s.key}>
            {localizedSpread(s, language).name}
          </option>
        ))}
      </select>
      {selectedCopy && (
        <div className="spread-desc">
          <span aria-hidden="true">✦</span>
          <p>{selectedCopy.description}</p>
          <small>
            {selectedCopy.card_count} {language === "zh" ? "张牌" : selectedCopy.card_count === 1 ? "card" : "cards"} · {selectedCopy.positions.join(" / ")}
          </small>
        </div>
      )}

      <label className="field-label" htmlFor="question-input">
        <span>02</span> {language === "zh" ? "写下你想询问的事" : "Write what you want to explore"}
      </label>
      <textarea
        id="question-input"
        value={question}
        onChange={(e) => onQuestionChange(e.target.value)}
        placeholder={language === "zh" ? "例如：我下半年的事业会有什么变化？" : "For example: What should I focus on in my career this year?"}
        rows={3}
      />

      {showStartButton && (
        <button className="primary" disabled={!question.trim() || !spreadKey} onClick={onStart}>
          {language === "zh" ? "开始占卜" : "Begin reading"} <span aria-hidden="true">✦</span>
        </button>
      )}

      {children}
    </div>
  );
}
