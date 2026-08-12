export type Orientation = "upright" | "reversed";

export interface Spread {
  key: string;
  name: string;
  card_count: number;
  positions: string[];
  logic: string;
  description: string;
}

export interface DrawnCard {
  card: string;
  orientation: Orientation;
}

export interface CardDisplay {
  name_zh: string;
  name_en: string;
  keyword: string;
}

export interface DrawResponse {
  cards: DrawnCard[];
  core_card: DrawnCard;
  positions: string[];
  display: CardDisplay[];
}

export interface InterpretationItem {
  position: string;
  card: string;
  interpretation: string;
}

export interface InterpretResponse {
  interpretations: InterpretationItem[];
  summary: string;
  reading_id: number;
}

export interface DeckCard {
  card: string;
  name_zh: string;
  name_en: string;
}

export interface VisionCard {
  card: string;
  orientation: Orientation;
  confidence: number;
  valid: boolean;
}

export interface VisionRecognizeResponse {
  success: boolean;
  cards: VisionCard[];
  error?: string | null;
}

export interface HistoryEntry {
  id: number;
  timestamp: string;
  question: string;
  spread: string;
  cards: DrawnCard[];
  core_card: string;
  single_interpretations: InterpretationItem[];
  summary: string;
}
