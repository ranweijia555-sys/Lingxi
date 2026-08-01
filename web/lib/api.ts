import type { DrawnCard, DrawResponse, InterpretResponse, Spread } from "./types";

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
