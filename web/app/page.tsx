"use client";

import Image from "next/image";
import { useEffect, useState } from "react";

import CardFan from "@/components/CardFan";
import CardSlot from "@/components/CardSlot";
import ModeToggle, { type ReadingMode } from "@/components/ModeToggle";
import PhotoRecognize from "@/components/PhotoRecognize";
import ReadingResult from "@/components/ReadingResult";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import SpreadPicker from "@/components/SpreadPicker";
import { drawCards, getSpreads, interpretReading, resolveVisionCards } from "@/lib/api";
import { cardImagePath } from "@/lib/card-images";
import { localizedSpread, useLanguage, type Language } from "@/lib/language";
import type { DrawnCard, DrawResponse, InterpretResponse, Spread } from "@/lib/types";

type Phase = "setup" | "drawing" | "revealed" | "interpreting" | "done";

const PHASE_COPY: Record<Language, Record<Exclude<Phase, "setup">, { eyebrow: string; title: string; note: string }>> = {
  zh: {
    drawing: { eyebrow: "THE DRAW", title: "让目光掠过牌阵", note: "停在最先让你产生感觉的位置，然后轻触它。" },
    revealed: { eyebrow: "THE REVEAL", title: "你的牌已经揭示", note: "先留意每张牌带来的第一印象。" },
    interpreting: { eyebrow: "THE READING", title: "牌意正在汇聚", note: "正在结合牌位、正逆位与核心牌整理这次阅读。" },
    done: { eyebrow: "THE READING", title: "这就是此刻的牌面", note: "保留与你有关的部分，也允许答案慢慢显现。" },
  },
  en: {
    drawing: { eyebrow: "THE DRAW", title: "Let your attention move across the deck", note: "Pause at the first card that creates a feeling, then select it." },
    revealed: { eyebrow: "THE REVEAL", title: "Your cards are revealed", note: "Notice the first impression each card gives you." },
    interpreting: { eyebrow: "THE READING", title: "The message is taking shape", note: "The positions, orientations, and core card are being read together." },
    done: { eyebrow: "THE READING", title: "A reflection for this moment", note: "Keep what feels relevant and allow the rest to unfold over time." },
  },
};

const HOME_COPY = {
  zh: {
    ritual: "A QUIET TAROT RITUAL",
    title: <>为此刻，<br />抽取一张回应</>,
    lede: "写下正在占据你心绪的问题。让牌面成为一面安静的镜子，照见线索、选择与仍未被说出的直觉。",
    begin: "BEGIN THE RITUAL",
    choose: "选择你的方式",
    question: "你的问题",
    spread: "当前牌阵",
    selected: "已选择",
    selectHint: "轻触任意牌背",
    reshuffle: "重新洗牌",
    reveal: "揭示牌面",
    thinking: "正在整理牌面之间的线索…",
    restart: "开始新的占卜",
    cards: "张牌",
    connectionError: "无法连接后端，请确认 API 服务已启动",
    drawError: "抽牌失败，请稍后重试",
    readingError: "解读失败，请稍后重试",
    questionError: "请先选择牌阵并输入问题",
    recognitionError: "识别结果确认失败，请稍后重试",
  },
  en: {
    ritual: "A QUIET TAROT RITUAL",
    title: <>Draw a reflection<br />for this moment</>,
    lede: "Write down what is occupying your mind. Let the cards become a quiet mirror for the choices, patterns, and intuition already present.",
    begin: "BEGIN THE RITUAL",
    choose: "Choose how to begin",
    question: "Your question",
    spread: "Selected spread",
    selected: "Selected",
    selectHint: "Select any card back",
    reshuffle: "Reshuffle",
    reveal: "Reveal cards",
    thinking: "Reading the connections between the cards…",
    restart: "Begin a new reading",
    cards: "cards",
    connectionError: "The reading service is unavailable. Please check that the API is running.",
    drawError: "The draw could not be completed. Please try again.",
    readingError: "The interpretation could not be completed. Please try again.",
    questionError: "Choose a spread and enter a question first.",
    recognitionError: "The recognized cards could not be confirmed. Please try again.",
  },
};

export default function Home() {
  const { language } = useLanguage();
  const copy = HOME_COPY[language];
  const [spreads, setSpreads] = useState<Spread[]>([]);
  const [spreadKey, setSpreadKey] = useState("");
  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState<ReadingMode>("draw");
  const [phase, setPhase] = useState<Phase>("setup");
  const [draw, setDraw] = useState<DrawResponse | null>(null);
  const [pickedCount, setPickedCount] = useState(0);
  const [result, setResult] = useState<InterpretResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [drawKey, setDrawKey] = useState(0);

  useEffect(() => {
    if (spreads.length) return;
    getSpreads()
      .then((list) => {
        setSpreads(list);
        if (list.length) setSpreadKey(list[0].key);
      })
      .catch(() => setError(copy.connectionError));
  }, [copy.connectionError, spreads.length]);

  const selectedSpread = spreads.find((spread) => spread.key === spreadKey);
  const selectedSpreadCopy = selectedSpread ? localizedSpread(selectedSpread, language) : undefined;

  async function runReveal(drawResponse: DrawResponse) {
    setPhase("revealed");
    setTimeout(() => setPhase("interpreting"), 420);
    try {
      const response = await interpretReading({
        question,
        spread_key: spreadKey,
        cards: drawResponse.cards,
        core_card: drawResponse.core_card,
        language,
      });
      setResult(response);
      setPhase("done");
    } catch {
      setError(copy.readingError);
      setPhase("revealed");
    }
  }

  async function handleStart() {
    if (!question.trim() || !spreadKey) return;
    setError(null);
    try {
      const response = await drawCards(spreadKey);
      setDraw(response);
      setPickedCount(0);
      setDrawKey((key) => key + 1);
      setPhase("drawing");
    } catch {
      setError(copy.drawError);
    }
  }

  async function handleRedraw() {
    if (!spreadKey) return;
    setError(null);
    try {
      const response = await drawCards(spreadKey);
      setDraw(response);
      setPickedCount(0);
      setDrawKey((key) => key + 1);
    } catch {
      setError(copy.drawError);
    }
  }

  async function handlePhotoConfirmed(cards: DrawnCard[]) {
    if (!question.trim() || !spreadKey) {
      setError(copy.questionError);
      return;
    }
    setError(null);
    try {
      const response = await resolveVisionCards(cards, spreadKey);
      setDraw(response);
      setPickedCount(response.cards.length);
      setDrawKey((key) => key + 1);
      await runReveal(response);
    } catch {
      setError(copy.recognitionError);
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

  if (phase === "setup") {
    return (
      <div className="site-shell landing-shell">
        <SiteHeader />
        <main className="landing-main">
          <section className="landing-intro">
            <div className="intro-copy animate-in">
              <span className="eyebrow">{copy.ritual}</span>
              <h1>{copy.title}</h1>
              <div className="celestial-rule" aria-hidden="true"><span>✦</span></div>
              <p className="intro-lede">
                {copy.lede}
              </p>
            </div>

            <div className="hero-card-scene animate-in animate-in-delay-1" aria-hidden="true">
              <div className="hero-card">
                <Image
                  src={cardImagePath("女祭司")}
                  alt=""
                  fill
                  priority
                  sizes="(max-width: 900px) 42vw, 310px"
                />
              </div>
            </div>
          </section>

          <section className="setup-section animate-in animate-in-delay-2" aria-labelledby="setup-title">
            <div className="section-label">
              <span>{copy.begin}</span>
              <h2 id="setup-title">{copy.choose}</h2>
            </div>
            <ModeToggle mode={mode} onChange={setMode} />
            <SpreadPicker
              spreads={spreads}
              spreadKey={spreadKey}
              onSpreadChange={setSpreadKey}
              question={question}
              onQuestionChange={setQuestion}
              onStart={handleStart}
              showStartButton={mode === "draw"}
            >
              {mode === "photo" && selectedSpread && (
                <PhotoRecognize expectedCount={selectedSpread.card_count} onConfirm={handlePhotoConfirmed} />
              )}
            </SpreadPicker>
            {error && <p className="error page-error">{error}</p>}
          </section>
        </main>
        <SiteFooter />
      </div>
    );
  }

  if (!draw || !selectedSpread) return null;

  const phaseCopy = PHASE_COPY[language][phase];
  const hasRevealed = phase === "revealed" || phase === "interpreting" || phase === "done";

  return (
    <div className={`site-shell reading-shell phase-${phase}`}>
      <SiteHeader />
      <main className="reading-main">
        <header className="reading-heading animate-in">
          <span className="eyebrow">{phaseCopy.eyebrow}</span>
          <h1>{phaseCopy.title}</h1>
          <p>{phaseCopy.note}</p>
          {error && <p className="error page-error">{error}</p>}
        </header>

        <div className="reading-workspace">
          <div className="reading-context animate-in animate-in-delay-1">
            <div>
              <span>{copy.question}</span>
              <p>{question}</p>
            </div>
            <div>
              <span>{copy.spread}</span>
              <p>{selectedSpreadCopy?.name}</p>
              <small>{selectedSpread.card_count} {copy.cards} · {selectedSpreadCopy?.positions.join(" / ")}</small>
            </div>
          </div>

          <section className="draw-canvas animate-in animate-in-delay-2" aria-label="抽牌区域">
            <div className="tray">
              {selectedSpreadCopy?.positions.map((label, index) => (
                <CardSlot
                  key={label}
                  index={index}
                  label={label}
                  revealed={hasRevealed}
                  isCore={index < pickedCount && draw.cards[index].card === draw.core_card.card}
                  card={
                    index < pickedCount
                      ? { orientation: draw.cards[index].orientation, display: draw.display[index] }
                      : undefined
                  }
                />
              ))}
            </div>

            {phase === "drawing" && (
              <>
                <div className="draw-instruction">
                  <span className="count">{copy.selected} <b>{pickedCount}</b> / {selectedSpread.card_count}</span>
                  <span>{copy.selectHint}</span>
                </div>
                <CardFan key={drawKey} totalPicks={selectedSpread.card_count} onPick={() => setPickedCount((count) => count + 1)} />
                <div className="controls">
                  <button className="ghost" onClick={handleRedraw}>{copy.reshuffle}</button>
                  <button
                    className="primary"
                    disabled={pickedCount < selectedSpread.card_count}
                    onClick={() => runReveal(draw)}
                  >
                    {copy.reveal} <span aria-hidden="true">✦</span>
                  </button>
                </div>
              </>
            )}

            {(phase === "interpreting" || phase === "done" || phase === "revealed") && (
              <div className="controls result-controls">
                {phase !== "done" && (
                  <span className="thinking"><i /> {copy.thinking}</span>
                )}
                {phase === "done" && (
                  <button className="ghost" onClick={handleRestart}>{copy.restart}</button>
                )}
              </div>
            )}
          </section>
        </div>

        {phase === "done" && result && <ReadingResult result={result} />}
      </main>
      <SiteFooter />
    </div>
  );
}
