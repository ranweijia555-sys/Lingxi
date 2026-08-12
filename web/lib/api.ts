import type {
  DeckCard,
  DrawnCard,
  DrawResponse,
  HistoryEntry,
  InterpretResponse,
  Spread,
  VisionRecognizeResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8001";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`${path} failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

async function upload<T>(path: string, formData: FormData): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    throw new Error(`${path} failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export function getSpreads(): Promise<Spread[]> {
  return request<Spread[]>("/api/spreads");
}

export function drawCards(spreadKey: string): Promise<DrawResponse> {
  return request<DrawResponse>("/api/draw", {
    method: "POST",
    body: JSON.stringify({ spread_key: spreadKey }),
  });
}

export function interpretReading(payload: {
  question: string;
  spread_key: string;
  cards: DrawnCard[];
  core_card: DrawnCard;
}): Promise<InterpretResponse> {
  return request<InterpretResponse>("/api/interpret", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getDeck(): Promise<DeckCard[]> {
  return request<DeckCard[]>("/api/deck");
}

export function recognizeCards(file: File, expectedCount?: number): Promise<VisionRecognizeResponse> {
  const formData = new FormData();
  formData.append("file", file);
  if (expectedCount) formData.append("expected_count", String(expectedCount));
  return upload<VisionRecognizeResponse>("/api/vision/recognize", formData);
}

export function resolveVisionCards(cards: DrawnCard[], spreadKey: string): Promise<DrawResponse> {
  return request<DrawResponse>("/api/vision/resolve", {
    method: "POST",
    body: JSON.stringify({ cards, spread_key: spreadKey }),
  });
}

export function getHistory(limit = 20): Promise<HistoryEntry[]> {
  return request<HistoryEntry[]>(`/api/history?limit=${limit}`);
}
