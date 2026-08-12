"""FastAPI 请求/响应模型"""
from typing import List, Literal, Optional

from pydantic import BaseModel

Orientation = Literal["upright", "reversed"]


class SpreadOut(BaseModel):
    key: str
    name: str
    card_count: int
    positions: List[str]
    logic: str
    description: str


class DrawRequest(BaseModel):
    spread_key: str


class CardOut(BaseModel):
    card: str
    orientation: Orientation


class CardDisplay(BaseModel):
    name_zh: str
    name_en: str
    keyword: str


class DrawResponse(BaseModel):
    cards: List[CardOut]
    core_card: CardOut
    positions: List[str]
    display: List[CardDisplay]


class InterpretRequest(BaseModel):
    question: str
    spread_key: str
    cards: List[CardOut]
    core_card: CardOut


class InterpretationItem(BaseModel):
    position: str
    card: str
    interpretation: str


class InterpretResponse(BaseModel):
    interpretations: List[InterpretationItem]
    summary: str
    reading_id: int


class DeckCardOut(BaseModel):
    card: str
    name_zh: str
    name_en: str


class VisionCardOut(BaseModel):
    card: str
    orientation: Orientation
    confidence: float
    valid: bool


class VisionRecognizeResponse(BaseModel):
    success: bool
    cards: List[VisionCardOut]
    error: Optional[str] = None


class ResolveRequest(BaseModel):
    cards: List[CardOut]
    spread_key: str


class HistoryEntry(BaseModel):
    id: int
    timestamp: str
    question: str
    spread: str
    cards: List[CardOut]
    core_card: str
    single_interpretations: List[InterpretationItem]
    summary: str
