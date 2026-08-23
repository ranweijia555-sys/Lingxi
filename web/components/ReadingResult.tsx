"use client";

import { localizedCardKey, useLanguage } from "@/lib/language";
import type { InterpretResponse } from "@/lib/types";

export default function ReadingResult({ result }: { result: InterpretResponse }) {
  const { language } = useLanguage();
  return (
    <div className="reading-result">
      <header className="result-heading">
        <span className="eyebrow">YOUR READING</span>
        <h2>{language === "zh" ? "牌面给出的回应" : "What the cards reflect"}</h2>
        <p>{language === "zh" ? "每一张牌先回应它所在的位置，最后再汇成完整的线索。" : "Each card speaks from its position before the reading comes together as a whole."}</p>
      </header>
      <div className="interpretation-list">
        {result.interpretations.map((item, i) => (
          <article className="interp-block" key={i}>
            <span className="interp-index">{String(i + 1).padStart(2, "0")}</span>
            <div>
              <div className="interp-title">
                <span>{item.position}</span>
                <strong>{localizedCardKey(item.card, language)}</strong>
              </div>
              <p>{item.interpretation}</p>
            </div>
          </article>
        ))}
      </div>
      <div className="summary-block">
        <span className="eyebrow">SYNTHESIS</span>
        <h3>{language === "zh" ? "综合启示" : "Synthesis"}</h3>
        <p>{result.summary}</p>
        <div className="summary-mark" aria-hidden="true">✦</div>
      </div>
      <p className="reading-id">
        <span aria-hidden="true">◇</span> {language === "zh" ? "此次占卜已归档" : "Reading saved to your archive"} · #{result.reading_id}
      </p>
    </div>
  );
}
