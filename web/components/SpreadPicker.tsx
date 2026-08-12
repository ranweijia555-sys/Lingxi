"use client";

import type { ReactNode } from "react";

import CornerFlourish from "@/components/CornerFlourish";
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

  return (
    <div className="setup-panel ornate-frame">
      <CornerFlourish className="corner-flourish tl" />
      <CornerFlourish className="corner-flourish tr" />
      <CornerFlourish className="corner-flourish bl" />
      <CornerFlourish className="corner-flourish br" />
      <label className="field-label" htmlFor="spread-select">
        选择牌阵
      </label>
      <select id="spread-select" value={spreadKey} onChange={(e) => onSpreadChange(e.target.value)}>
        {spreads.map((s) => (
          <option key={s.key} value={s.key}>
            {s.name}
          </option>
        ))}
      </select>
      {selected && <p className="spread-desc">💡 {selected.description}</p>}

      <label className="field-label" htmlFor="question-input">
        你想问什么？
      </label>
      <textarea
        id="question-input"
        value={question}
        onChange={(e) => onQuestionChange(e.target.value)}
        placeholder="例如：我下半年的事业会有什么变化？"
        rows={3}
      />

      {showStartButton && (
        <button className="primary" disabled={!question.trim() || !spreadKey} onClick={onStart}>
          ✦ 开始占卜 ✦
        </button>
      )}

      {children}
    </div>
  );
}
