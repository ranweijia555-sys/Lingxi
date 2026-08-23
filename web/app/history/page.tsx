"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHistory } from "@/lib/api";
import { localizedCardKey, localizedSpreadName, useLanguage } from "@/lib/language";
import type { HistoryEntry } from "@/lib/types";

function formatDate(iso: string, locale: string) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString(locale, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function HistoryPage() {
  const { language } = useLanguage();
  const copy = language === "zh" ? {
    title: "占卜档案",
    intro: "回看过去的提问与牌面，寻找重复出现的主题和已经发生的变化。",
    back: "返回占卜台",
    loadError: "无法加载历史记录，请确认 API 服务已启动",
    loading: "加载中…",
    emptyTitle: "档案仍是空白",
    emptyCopy: "完成第一次占卜后，牌面与解读会保存在这里。",
    emptyAction: "开始第一次占卜",
    core: "核心牌",
    synthesis: "综合启示",
  } : {
    title: "Reading Archive",
    intro: "Return to earlier questions and notice the themes, changes, and patterns that recur over time.",
    back: "Back to reading",
    loadError: "The archive could not be loaded. Please check that the API is running.",
    loading: "Loading…",
    emptyTitle: "The archive is still empty",
    emptyCopy: "Your cards and interpretation will appear here after the first reading.",
    emptyAction: "Begin the first reading",
    core: "Core card",
    synthesis: "Synthesis",
  };
  const [entries, setEntries] = useState<HistoryEntry[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<number | null>(null);

  useEffect(() => {
    if (entries !== null) return;
    getHistory(30)
      .then(setEntries)
      .catch(() => setError(copy.loadError));
  }, [copy.loadError, entries]);

  return (
    <div className="site-shell history-shell">
      <SiteHeader active="history" />
      <main className="history-main">
        <header className="history-heading animate-in">
          <span className="eyebrow">THE ARCHIVE</span>
          <h1>{copy.title}</h1>
          <p>{copy.intro}</p>
          <Link href="/" className="text-link">{copy.back} <span aria-hidden="true">✦</span></Link>
          {error && <p className="error page-error">{error}</p>}
        </header>

        <div className="archive-rule" aria-hidden="true"><span>READINGS</span><i /></div>
        <div className="history-list">
        {entries === null && !error && <p className="count">{copy.loading}</p>}
        {entries?.length === 0 && (
          <div className="empty-state">
            <span aria-hidden="true">◇</span>
            <h2>{copy.emptyTitle}</h2>
            <p>{copy.emptyCopy}</p>
            <Link className="primary link-button" href="/">{copy.emptyAction}</Link>
          </div>
        )}
        {entries?.map((entry) => {
          const isOpen = expanded === entry.id;
          return (
            <div className={`history-item ${isOpen ? "open" : ""}`} key={entry.id}>
              <button className="history-item-header" onClick={() => setExpanded(isOpen ? null : entry.id)}>
                <span className="history-index">{String(entry.id).padStart(3, "0")}</span>
                <div className="history-item-main">
                  <div className="history-item-meta">
                    <span className="history-item-date">{formatDate(entry.timestamp, language === "zh" ? "zh-CN" : "en-AU")}</span>
                    <span className="history-item-spread">{localizedSpreadName(entry.spread, language)}</span>
                  </div>
                  <div className="history-item-question">{entry.question}</div>
                  <div className="history-item-core">{copy.core} · {localizedCardKey(entry.core_card, language)}</div>
                </div>
                <span className="history-toggle" aria-hidden="true">{isOpen ? "−" : "+"}</span>
              </button>

              {isOpen && (
                <div className="history-item-body">
                  {entry.single_interpretations.map((item, i) => (
                    <article className="archive-interpretation" key={i}>
                      <span>{String(i + 1).padStart(2, "0")}</span>
                      <div>
                      <div className="interp-title">
                        {item.position} · {localizedCardKey(item.card, language)}
                      </div>
                      <p>{item.interpretation}</p>
                      </div>
                    </article>
                  ))}
                  <div className="summary-block">
                    <span className="eyebrow">SYNTHESIS</span>
                    <h3>{copy.synthesis}</h3>
                    <p>{entry.summary}</p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}
