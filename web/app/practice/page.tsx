"use client";

import Link from "next/link";

import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { useLanguage } from "@/lib/language";

const PRACTICE_COPY = {
  zh: {
    eyebrow: "THE READER'S TABLE",
    title: <>我如何，<br />阅读一副牌</>,
    intro: "我把塔罗看作一门关于关系的语言。单张牌提供象征，牌阵给出位置，而真正的阅读发生在它们彼此呼应、抵触和转变的地方。",
    signature: "我的牌桌，不负责替你预言一个无法改变的结局。它更像一面镜子：帮助你看见此刻正在发生什么、什么仍未被说出，以及下一步有哪些可能。",
    foundationEyebrow: "MY FOUNDATION",
    foundationTitle: "阅读从问题开始，而不是从答案开始",
    foundationBody: "在翻牌以前，我会先寻找问题真正指向的核心。一个关于关系的问题，也许实际在询问边界；一个关于事业的问题，也许真正关心的是安全感。问题越清楚，牌面提供的线索就越有方向。",
    sequenceEyebrow: "THE READING SEQUENCE",
    sequenceTitle: "一次阅读的五个判断层次",
    sequence: [
      { number: "01", title: "问题与边界", body: "确认你真正想理解的事，也区分塔罗能够照见的部分与需要现实行动验证的部分。" },
      { number: "02", title: "牌位与方向", body: "先尊重牌阵给予每张牌的职责，再观察正位、逆位如何改变能量的表达方式。" },
      { number: "03", title: "画面与第一直觉", body: "人物朝向、颜色、动作与最先吸引目光的细节，往往揭示问题中尚未进入语言的部分。" },
      { number: "04", title: "结构与核心牌", body: "比较元素、数字和大阿卡纳的重量，寻找重复、缺失、冲突，以及能够统领整组牌的核心牌。" },
      { number: "05", title: "整合成回应", body: "最后才回到传统牌义，把所有线索编织成一条与你的问题有关、同时保留选择空间的叙事。" },
    ],
    relationEyebrow: "BETWEEN THE CARDS",
    relationTitle: "我读的不是三张孤立的牌",
    relationBody: "当火与水同时出现，我会留意行动和感受是否彼此拉扯；当数字连续，我会观察事情正处于哪个发展阶段；当人物彼此背离或望向同一方向，画面本身也在描述关系。牌义不会被机械相加，它们会组成一句新的话。",
    lenses: [
      { symbol: "△", title: "元素", body: "火、水、风、土告诉我能量集中在哪里，又缺少了什么。" },
      { symbol: "Ⅸ", title: "数字", body: "1–9 的循环帮助我判断开始、推进、停滞与完成。" },
      { symbol: "☾", title: "星体", body: "占星对应补充能量的气质，但不会覆盖牌面本身。" },
      { symbol: "✦", title: "直觉", body: "直觉提出线索，结构负责检验它是否与整组牌相符。" },
    ],
    aiEyebrow: "THE HUMAN FRAMEWORK",
    aiTitle: "这套体系先有我的判断，再有文字的整理",
    aiBody: "牌阵结构、核心牌判断、元素关系、数字归元与解读顺序，来自我建立的阅读框架。系统会协助把这些线索组织成清楚的文字，但不会替你作决定，也不会把塔罗包装成确定的命运。最终值得保留的，是那些真正帮助你理解自身处境的部分。",
    closing: "如果你已经准备好，就带着一个诚实的问题回到牌桌。",
    action: "回到牌桌开始占卜",
  },
  en: {
    eyebrow: "THE READER'S TABLE",
    title: <>How I read<br />a spread</>,
    intro: "I read tarot as a language of relationships. A card offers a symbol, a spread gives it a position, and the reading happens where those symbols echo, resist, and transform one another.",
    signature: "My table is not here to predict an unchangeable ending. It is a mirror for what is present now, what has not yet been said, and which possibilities remain open to you.",
    foundationEyebrow: "MY FOUNDATION",
    foundationTitle: "The reading begins with the question, not the answer",
    foundationBody: "Before a card is turned, I look for what the question is truly asking. A question about a relationship may be about boundaries; a question about work may be about security. The clearer the question, the more direction the cards can offer.",
    sequenceEyebrow: "THE READING SEQUENCE",
    sequenceTitle: "Five layers in every reading",
    sequence: [
      { number: "01", title: "Question & boundary", body: "Clarify what you genuinely want to understand, and distinguish reflection from what must be tested through real action." },
      { number: "02", title: "Position & orientation", body: "Respect the role assigned by the spread, then observe how upright or reversed energy changes its expression." },
      { number: "03", title: "Image & first impression", body: "Direction, colour, gesture, and the first detail that catches the eye can reveal what has not yet become language." },
      { number: "04", title: "Pattern & core card", body: "Compare elements, numbers, and Major Arcana weight to find repetition, absence, tension, and the card anchoring the spread." },
      { number: "05", title: "A coherent response", body: "Only then do traditional meanings return, woven into a response that is relevant while preserving your agency." },
    ],
    relationEyebrow: "BETWEEN THE CARDS",
    relationTitle: "I am not reading three isolated cards",
    relationBody: "When Fire and Water meet, I look for tension between action and feeling. When numbers form a sequence, I look for a stage of development. When figures turn away from or face one another, the image itself describes a relationship. Meanings are not mechanically added; together, the cards make a new sentence.",
    lenses: [
      { symbol: "△", title: "Elements", body: "Fire, Water, Air, and Earth show where energy gathers and what is missing." },
      { symbol: "Ⅸ", title: "Numbers", body: "The 1–9 cycle helps locate beginnings, momentum, pauses, and completion." },
      { symbol: "☾", title: "The sky", body: "Astrological correspondences add tone without overriding the image before us." },
      { symbol: "✦", title: "Intuition", body: "Intuition proposes a clue; structure tests whether it belongs to the whole spread." },
    ],
    aiEyebrow: "THE HUMAN FRAMEWORK",
    aiTitle: "The method begins with my judgement; language comes after",
    aiBody: "The spread structure, core-card logic, elemental relationships, numerical reduction, and reading sequence come from the framework I have built. The system helps arrange these clues into clear language, but it does not make decisions for you or present tarot as fixed fate. What matters is the part that genuinely helps you understand your situation.",
    closing: "When you are ready, return to the table with one honest question.",
    action: "Return to the table",
  },
};

export default function PracticePage() {
  const { language } = useLanguage();
  const copy = PRACTICE_COPY[language];

  return (
    <div className="site-shell practice-shell">
      <SiteHeader active="practice" />
      <main className="practice-main">
        <header className="practice-hero animate-in">
          <div className="practice-hero-copy">
            <span className="eyebrow">{copy.eyebrow}</span>
            <h1>{copy.title}</h1>
            <div className="celestial-rule" aria-hidden="true"><span>✦</span></div>
            <p className="practice-intro">{copy.intro}</p>
          </div>
          <blockquote className="reader-note">
            <span aria-hidden="true">☾</span>
            <p>{copy.signature}</p>
            <footer>— ASTRA</footer>
          </blockquote>
        </header>

        <section className="practice-foundation animate-in animate-in-delay-1">
          <div className="practice-section-heading">
            <span className="eyebrow">{copy.foundationEyebrow}</span>
            <h2>{copy.foundationTitle}</h2>
          </div>
          <p>{copy.foundationBody}</p>
        </section>

        <section className="practice-sequence">
          <div className="practice-section-heading">
            <span className="eyebrow">{copy.sequenceEyebrow}</span>
            <h2>{copy.sequenceTitle}</h2>
          </div>
          <ol className="practice-steps">
            {copy.sequence.map((step) => (
              <li key={step.number}>
                <span>{step.number}</span>
                <div><h3>{step.title}</h3><p>{step.body}</p></div>
              </li>
            ))}
          </ol>
        </section>

        <section className="practice-relations">
          <div className="practice-relation-copy">
            <span className="eyebrow">{copy.relationEyebrow}</span>
            <h2>{copy.relationTitle}</h2>
            <p>{copy.relationBody}</p>
          </div>
          <div className="reading-lenses">
            {copy.lenses.map((lens) => (
              <article key={lens.title}>
                <span aria-hidden="true">{lens.symbol}</span>
                <h3>{lens.title}</h3>
                <p>{lens.body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="human-framework">
          <span className="framework-mark" aria-hidden="true">✦</span>
          <span className="eyebrow">{copy.aiEyebrow}</span>
          <h2>{copy.aiTitle}</h2>
          <p>{copy.aiBody}</p>
        </section>

        <footer className="practice-closing">
          <p>{copy.closing}</p>
          <Link className="practice-action" href="/">{copy.action}<span aria-hidden="true">✦</span></Link>
        </footer>
      </main>
      <SiteFooter />
    </div>
  );
}
