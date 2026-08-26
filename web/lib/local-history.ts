import type { DrawnCard, HistoryEntry, InterpretResponse } from "./types";
import type { Language } from "./language";

const STORAGE_KEY = "lingxi-private-readings-v1";
const MAX_ENTRIES = 100;

function isHistoryEntry(value: unknown): value is HistoryEntry {
  if (!value || typeof value !== "object") return false;
  const entry = value as Partial<HistoryEntry>;
  return (
    typeof entry.id === "string" &&
    typeof entry.timestamp === "string" &&
    typeof entry.question === "string" &&
    typeof entry.spread === "string" &&
    Array.isArray(entry.cards) &&
    typeof entry.core_card === "string" &&
    Array.isArray(entry.single_interpretations) &&
    typeof entry.summary === "string"
  );
}

export function getLocalHistory(): HistoryEntry[] {
  if (typeof window === "undefined") return [];
  try {
    const parsed: unknown = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]");
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(isHistoryEntry).sort((a, b) => b.timestamp.localeCompare(a.timestamp));
  } catch {
    return [];
  }
}

export function saveLocalReading(input: {
  question: string;
  spreadKey: string;
  spreadName: string;
  cards: DrawnCard[];
  coreCard: DrawnCard;
  result: InterpretResponse;
  language: Language;
}): HistoryEntry {
  const entry: HistoryEntry = {
    id: crypto.randomUUID(),
    timestamp: new Date().toISOString(),
    question: input.question,
    spread: input.spreadName,
    spread_key: input.spreadKey,
    language: input.language,
    cards: input.cards,
    core_card: input.coreCard.card,
    single_interpretations: input.result.interpretations,
    summary: input.result.summary,
  };
  const entries = [entry, ...getLocalHistory().filter((item) => item.id !== entry.id)].slice(0, MAX_ENTRIES);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
  return entry;
}

export function clearLocalHistory() {
  if (typeof window !== "undefined") localStorage.removeItem(STORAGE_KEY);
}
