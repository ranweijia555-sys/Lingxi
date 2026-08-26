"""FastAPI 请求/响应模型"""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

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
    language: Literal["zh", "en"] = "zh"


class InterpretationItem(BaseModel):
    position: str
    card: str
    interpretation: str


class InterpretResponse(BaseModel):
    interpretations: List[InterpretationItem]
    summary: str


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


class UsageEventRequest(BaseModel):
    anonymous_id: str = Field(min_length=16, max_length=128)
    session_id: str = Field(min_length=16, max_length=128)
    event: Literal["reading_started", "reading_completed", "reading_failed"]
    spread_key: Optional[str] = Field(default=None, max_length=64)
    mode: Optional[Literal["draw", "photo"]] = None
    language: Literal["zh", "en"] = "zh"
    client_reading_id: Optional[str] = Field(default=None, min_length=16, max_length=128)


class FeedbackRequest(BaseModel):
    anonymous_id: str = Field(min_length=16, max_length=128)
    session_id: str = Field(min_length=16, max_length=128)
    rating: Literal["helpful", "neutral", "not_helpful"]
    comment: Optional[str] = Field(default=None, max_length=500)
    spread_key: str = Field(min_length=1, max_length=64)
    mode: Literal["draw", "photo"]
    language: Literal["zh", "en"] = "zh"
    client_reading_id: str = Field(min_length=16, max_length=128)


class AcceptedResponse(BaseModel):
    accepted: bool
