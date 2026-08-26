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

const HERO_CARD_POOL = [
  "女祭司",
  "愚者",
  "魔术师",
  "皇后",
  "恋人",
  "战车",
  "力量",
  "隐士",
  "命运之轮",
  "星星",
  "月亮",
  "太阳",
  "世界",
];

const TAROT_SYSTEM_COPY = {
  zh: {
    eyebrow: "TAROT SYSTEM",
    summary: "78 张牌 · 牌阵位置 · 四元素 · 灵数与占星",
    expand: "展开塔罗体系",
    steps: [
      { number: "01", title: "牌位与核心牌", detail: "先看每张牌所在的位置与正、逆位；多牌阅读再找出贯穿全局的核心牌。" },
      { number: "02", title: "四元素", detail: "权杖属火，关注行动；圣杯属水，关注感受；宝剑属风，关注思想；星币属土，关注现实。" },
      { number: "03", title: "灵数与占星", detail: "数字牌归元至 1–9 观察发展阶段，大阿卡纳再结合星体与星座对应理解能量主题。" },
    ],
    boundary: "牌义不是孤立的固定答案；牌位、元素之间的呼应与冲突，才共同组成这次阅读的线索。",
  },
  en: {
    eyebrow: "TAROT SYSTEM",
    summary: "78 cards · spread positions · four elements · numerology and astrology",
    expand: "Explore the tarot system",
    steps: [
      { number: "01", title: "Position & core", detail: "Each card is read through its spread position and orientation; a core card anchors a multi-card reading." },
      { number: "02", title: "Four elements", detail: "Wands/Fire speak to action, Cups/Water to feeling, Swords/Air to thought, and Pentacles/Earth to lived reality." },
      { number: "03", title: "Number & sky", detail: "Numbers reduce to 1–9 to show stages of development, while Major Arcana correspondences add planetary and zodiac themes." },
    ],
    boundary: "No card is a fixed answer in isolation; the relationships and tensions among positions and elements form the reading.",
  },
};

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
  const systemCopy = TAROT_SYSTEM_COPY[language];
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
  const [heroFlipped, setHeroFlipped] = useState(false);
  const [heroCard, setHeroCard] = useState("女祭司");

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

  function chooseNextHeroCard() {
    setHeroCard((currentCard) => {
      const choices = HERO_CARD_POOL.filter((card) => card !== currentCard);
      return choices[Math.floor(Math.random() * choices.length)];
    });
  }

  function handleHeroClick() {
    if (heroFlipped) chooseNextHeroCard();
    setHeroFlipped((flipped) => !flipped);
  }

  if (phase === "setup") {
    return (
      <div className="site-shell landing-shell">
        <SiteHeader />
        <main className="landing-main">
          <section className="ritual-workspace" aria-labelledby="setup-title">
            <div className="ritual-form-column">
              <div className="intro-copy animate-in">
                <span className="eyebrow">{copy.ritual}</span>
                <h1 className={`ritual-title ritual-title-${language}`}>
                  {language === "zh" ? (
                    <>
                      <span className="ritual-title-line">
                        {["为", "此", "刻", "，"].map((character) => (
                          <span className="ritual-title-glyph" key={character}>{character}</span>
                        ))}
                      </span>
                      <span className="ritual-title-line">
                        {["抽", "取", "一", "张", "回", "应"].map((character) => (
                          <span className="ritual-title-glyph" key={character}>{character}</span>
                        ))}
                      </span>
                    </>
                  ) : copy.title}
                </h1>
                <div className="celestial-rule" aria-hidden="true"><span>✦</span></div>
                <p className="intro-lede">{copy.lede}</p>
                <details className="method-note">
                  <summary>
                    <span className="method-kicker">{systemCopy.eyebrow}</span>
                    <strong>{systemCopy.summary}</strong>
                    <span className="method-toggle" aria-label={systemCopy.expand}>+</span>
                  </summary>
                  <div className="method-body">
                    <ol className="method-steps">
                      {systemCopy.steps.map((step) => (
                        <li key={step.number}>
                          <span>{step.number}</span>
                          <strong>{step.title}</strong>
                          <p>{step.detail}</p>
                        </li>
                      ))}
                    </ol>
                    <p className="method-boundary"><span aria-hidden="true">✦</span>{systemCopy.boundary}</p>
                  </div>
                </details>
              </div>

              <div className="setup-section animate-in animate-in-delay-1">
                <div className="section-label sr-only">
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
              </div>
            </div>

            <aside className="hero-card-scene animate-in animate-in-delay-2">
              <span className="card-orbit card-orbit-one" aria-hidden="true" />
              <span className="card-orbit card-orbit-two" aria-hidden="true" />
              <button
                type="button"
                className={`hero-card${heroFlipped ? " is-flipped" : ""}`}
                onClick={handleHeroClick}
                onMouseLeave={() => {
                  if (!heroFlipped) chooseNextHeroCard();
                }}
                aria-label={language === "zh" ? `翻转${heroCard}，查看牌背` : `Flip ${heroCard} to view the card back`}
                aria-pressed={heroFlipped}
              >
                <span className="hero-card-inner">
                  <span className="hero-card-face hero-card-front">
                    <Image
                      key={heroCard}
                      src={cardImagePath(heroCard)}
                      alt={language === "zh" ? `${heroCard}塔罗牌` : `${heroCard} tarot card`}
                      fill
                      priority
                      sizes="(max-width: 640px) 58vw, (max-width: 900px) 34vw, 300px"
                    />
                  </span>
                  <span className="hero-card-face hero-card-back">
                    <Image
                      src={cardImagePath("牌背")}
                      alt=""
                      fill
                      sizes="(max-width: 640px) 58vw, (max-width: 900px) 34vw, 300px"
                    />
                  </span>
                </span>
              </button>
              <div className="hero-card-note">
                <span aria-hidden="true">☾</span>
                <p>{language === "zh" ? "每次翻转，遇见不同的牌" : "Each turn reveals another card"}</p>
              </div>
            </aside>
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
