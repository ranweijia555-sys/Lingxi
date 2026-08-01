"use client";

import { useEffect, useState } from "react";

import CardFan from "@/components/CardFan";
import CardSlot from "@/components/CardSlot";
import ReadingResult from "@/components/ReadingResult";
import SpreadPicker from "@/components/SpreadPicker";
import { drawCards, getSpreads, interpretReading } from "@/lib/api";
import type { DrawResponse, InterpretResponse, Spread } from "@/lib/types";

type Phase = "setup" | "drawing" | "revealed" | "interpreting" | "done";

export default function Home() {
  const [spreads, setSpreads] = useState<Spread[]>([]);
  const [spreadKey, setSpreadKey] = useState("");
  const [question, setQuestion] = useState("");
  const [phase, setPhase] = useState<Phase>("setup");
  const [draw, setDraw] = useState<DrawResponse | null>(null);
  const [pickedCount, setPickedCount] = useState(0);
  const [result, setResult] = useState<InterpretResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [drawKey, setDrawKey] = useState(0);

  useEffect(() => {
    getSpreads()
      .then((list) => {
        setSpreads(list);
        if (list.length) setSpreadKey(list[0].key);
      })
      .catch(() => setError("无法连接后端，请确认 API 服务已启动"));
  }, []);

  const selectedSpread = spreads.find((s) => s.key === spreadKey);

  async function handleStart() {
    if (!question.trim() || !spreadKey) return;
    setError(null);
    try {
      const res = await drawCards(spreadKey);
      setDraw(res);
      setPickedCount(0);
      setDrawKey((k) => k + 1);
      setPhase("drawing");
    } catch {
      setError("抽牌失败，请稍后重试");
    }
  }

  async function handleRedraw() {
    if (!spreadKey) return;
    try {
      const res = await drawCards(spreadKey);
      setDraw(res);
      setPickedCount(0);
      setDrawKey((k) => k + 1);
    } catch {
      setError("抽牌失败，请稍后重试");
    }
  }

  function handlePick() {
    setPickedCount((c) => c + 1);
  }

  async function handleReveal() {
    if (!draw) return;
    setPhase("revealed");
    setTimeout(() => setPhase("interpreting"), 300);
    try {
      const res = await interpretReading({
        question,
        spread_key: spreadKey,
        cards: draw.cards,
        core_card: draw.core_card,
      });
      setResult(res);
      setPhase("done");
    } catch {
      setError("解读失败，请稍后重试");
      setPhase("revealed");
    }
  }

  function handleRestart() {
    setPhase("setup");
    setDraw(null);
    setResult(null);
    setPickedCount(0);
    setQuestion("");
    setError(null);
  }

  return (
    <main>
      <header>
        <div className="mark">灵案 · AstRa</div>
        <h1>{phase === "setup" ? "抽取你的牌" : "扫过牌阵，感受呼应你的那一张"}</h1>
        {error && <p className="error">{error}</p>}
      </header>

      {phase === "setup" && (
        <SpreadPicker
          spreads={spreads}
          spreadKey={spreadKey}
          onSpreadChange={setSpreadKey}
          question={question}
          onQuestionChange={setQuestion}
          onStart={handleStart}
        />
      )}

      {phase !== "setup" && draw && selectedSpread && (
        <>
          <div className="tray">
            {selectedSpread.positions.map((label, i) => (
              <CardSlot
                key={i}
                index={i}
                label={label}
                revealed={phase === "revealed" || phase === "interpreting" || phase === "done"}
                isCore={i < pickedCount && draw.cards[i].card === draw.core_card.card}
                card={
                  i < pickedCount
                    ? { orientation: draw.cards[i].orientation, display: draw.display[i] }
                    : undefined
                }
              />
            ))}
          </div>

          {phase === "drawing" && (
            <>
              <CardFan key={drawKey} totalPicks={selectedSpread.card_count} onPick={handlePick} />
              <div className="controls">
                <span className="count">
                  已选 <b>{pickedCount}</b> / {selectedSpread.card_count}
                </span>
                <button
                  className="primary"
                  disabled={pickedCount < selectedSpread.card_count}
                  onClick={handleReveal}
                >
                  揭示 {selectedSpread.card_count} 张
                </button>
                <button className="ghost" onClick={handleRedraw}>
                  重新抽牌
                </button>
              </div>
            </>
          )}

          {(phase === "interpreting" || phase === "done") && (
            <div className="controls">
              {phase === "interpreting" && <span className="count">🌙 塔罗师正在沉思…</span>}
              {phase === "done" && (
                <button className="ghost" onClick={handleRestart}>
                  ⊹ 再来一次 ⊹
                </button>
              )}
            </div>
          )}

          {phase === "done" && result && <ReadingResult result={result} />}
        </>
      )}
    </main>
  );
}
