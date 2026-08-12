"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import WaveRule from "@/components/WaveRule";
import { getHistory } from "@/lib/api";
import type { HistoryEntry } from "@/lib/types";

function formatDate(iso: string) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function HistoryPage() {
  const [entries, setEntries] = useState<HistoryEntry[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<number | null>(null);

  useEffect(() => {
    getHistory(30)
      .then(setEntries)
      .catch(() => setError("无法加载历史记录，请确认 API 服务已启动"));
  }, []);

  return (
    <main>
      <header>
        <div className="mark">灵案 · AstRa</div>
        <h1>历史记录</h1>
        <WaveRule />
        <Link href="/" className="history-link">
          ← 返回抽牌
        </Link>
        {error && <p className="error">{error}</p>}
      </header>

      <div className="history-list">
        {entries === null && !error && <p className="count">加载中…</p>}
        {entries?.length === 0 && <p className="count">还没有占卜记录</p>}
        {entries?.map((entry) => {
          const isOpen = expanded === entry.id;
          return (
            <div className={`history-item ${isOpen ? "open" : ""}`} key={entry.id}>
              <button className="history-item-header" onClick={() => setExpanded(isOpen ? null : entry.id)}>
                <div className="history-item-meta">
                  <span className="history-item-date">{formatDate(entry.timestamp)}</span>
                  <span className="history-item-spread">{entry.spread}</span>
                </div>
                <div className="history-item-question">{entry.question}</div>
                <div className="history-item-core">核心牌 · {entry.core_card}</div>
              </button>

              {isOpen && (
                <div className="history-item-body">
                  {entry.single_interpretations.map((item, i) => (
                    <div className="interp-block" key={i}>
                      <div className="interp-title">
                        {item.position} · {item.card}
                      </div>
                      <p>{item.interpretation}</p>
                    </div>
                  ))}
                  <div className="summary-block">
                    <p>{entry.summary}</p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </main>
  );
}
