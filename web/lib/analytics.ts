import type { Language } from "./language";

const ANONYMOUS_ID_KEY = "lingxi-anonymous-id-v1";

export type ReadingMode = "draw" | "photo";
export type UsageEventName = "reading_started" | "reading_completed" | "reading_failed";
export type FeedbackRating = "helpful" | "neutral" | "not_helpful";

let sessionId: string | null = null;

function getAnonymousId() {
  let value = localStorage.getItem(ANONYMOUS_ID_KEY);
  if (!value) {
    value = crypto.randomUUID();
    localStorage.setItem(ANONYMOUS_ID_KEY, value);
  }
  return value;
}

function getSessionId() {
  sessionId ??= crypto.randomUUID();
  return sessionId;
}

async function post(path: string, body: object) {
  const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8001";
  const response = await fetch(`${apiBase}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`${path} failed: ${response.status}`);
}

export function trackUsageEvent(input: {
  event: UsageEventName;
  spreadKey?: string;
  mode?: ReadingMode;
  language: Language;
  readingId?: string;
}) {
  if (typeof window === "undefined") return Promise.resolve();
  return post("/api/analytics/event", {
    anonymous_id: getAnonymousId(),
    session_id: getSessionId(),
    event: input.event,
    spread_key: input.spreadKey,
    mode: input.mode,
    language: input.language,
    client_reading_id: input.readingId,
  });
}

export function submitReadingFeedback(input: {
  rating: FeedbackRating;
  comment?: string;
  spreadKey: string;
  mode: ReadingMode;
  language: Language;
  readingId: string;
}) {
  return post("/api/analytics/feedback", {
    anonymous_id: getAnonymousId(),
    session_id: getSessionId(),
    rating: input.rating,
    comment: input.comment?.trim() || null,
    spread_key: input.spreadKey,
    mode: input.mode,
    language: input.language,
    client_reading_id: input.readingId,
  });
}
