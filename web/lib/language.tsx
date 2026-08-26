"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export type Language = "zh" | "en";

const LanguageContext = createContext<{
  language: Language;
  setLanguage: (language: Language) => void;
} | null>(null);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>("zh");

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      const saved = localStorage.getItem("lingxi-language");
      if (saved === "zh" || saved === "en") {
        setLanguageState(saved);
        document.documentElement.lang = saved === "zh" ? "zh-CN" : "en";
      }
    });
    return () => cancelAnimationFrame(frame);
  }, []);

  function setLanguage(nextLanguage: Language) {
    setLanguageState(nextLanguage);
    localStorage.setItem("lingxi-language", nextLanguage);
    document.documentElement.lang = nextLanguage === "zh" ? "zh-CN" : "en";
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const value = useContext(LanguageContext);
  if (!value) throw new Error("useLanguage must be used within LanguageProvider");
  return value;
}

const SPREAD_EN = {
  single: {
    name: "Single Card Guidance",
    positions: ["Guidance"],
    description: "A concise prompt for the energy and perspective most useful right now.",
  },
  three_no_spread: {
    name: "Three Card Open Reading",
    positions: ["Card One", "Card Two", "Card Three"],
    description: "Three cards without fixed positions, read together as one flexible message.",
  },
  three_timeline: {
    name: "Past · Present · Future",
    positions: ["Past", "Present", "Future"],
    description: "A timeline reading that follows how the situation has moved and may continue to unfold.",
  },
} satisfies Record<string, { name: string; positions: string[]; description: string }>;

export function localizedSpread<T extends { key: string; name: string; positions: string[]; description: string }>(
  spread: T,
  language: Language,
) {
  if (language === "zh") return spread;
  const translated = SPREAD_EN[spread.key as keyof typeof SPREAD_EN];
  return translated ? { ...spread, ...translated } : spread;
}

const SPREAD_NAMES: Record<string, { zh: string; en: string }> = {
  single: { zh: "单张指引", en: "Single Card Guidance" },
  three_no_spread: { zh: "三张无牌阵", en: "Three Card Open Reading" },
  three_timeline: { zh: "三张时间线", en: "Past · Present · Future" },
  "单张指引": { zh: "单张指引", en: "Single Card Guidance" },
  "三张无牌阵": { zh: "三张无牌阵", en: "Three Card Open Reading" },
  "三张时间线": { zh: "三张时间线", en: "Past · Present · Future" },
  "Single Card Guidance": { zh: "单张指引", en: "Single Card Guidance" },
  "Three Card Open Reading": { zh: "三张无牌阵", en: "Three Card Open Reading" },
  "Past · Present · Future": { zh: "三张时间线", en: "Past · Present · Future" },
};

export function localizedSpreadName(name: string, language: Language) {
  return SPREAD_NAMES[name]?.[language] ?? name;
}

export function localizedCardKey(card: string, language: Language) {
  const chineseStart = card.search(/[\u3400-\u9fff]/);
  if (chineseStart < 0) return card;
  return language === "zh" ? card.slice(chineseStart).trim() : card.slice(0, chineseStart).trim();
}
