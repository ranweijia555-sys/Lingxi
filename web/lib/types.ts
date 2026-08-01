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
