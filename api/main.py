"""灵案 AstRa - FastAPI 后端（供 Next.js 抽牌页调用，逻辑复用 tarot/ 包）"""
import os
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from tarot.data_loader import load_full_deck, load_spreads
from tarot.drawer import draw_cards, find_core_card
from tarot.interpreter import interpret_single_card, synthesize_reading
from tarot.vision import recognize_cards

from api.telemetry import TelemetryUnavailable, anonymous_hash, insert_row
from api.schemas import (
    AcceptedResponse,
    CardDisplay,
    CardOut,
    DeckCardOut,
    DrawRequest,
    DrawResponse,
    FeedbackRequest,
    InterpretationItem,
    InterpretRequest,
    InterpretResponse,
    ResolveRequest,
    SpreadOut,
    UsageEventRequest,
    VisionCardOut,
    VisionRecognizeResponse,
)

app = FastAPI(title="灵案 AstRa API")

_default_origins = "http://localhost:3000,http://localhost:3001"
_allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", _default_origins).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

FULL_DECK = load_full_deck()

POSITION_EN = {
    "今日指引": "Guidance",
    "牌一": "Card One",
    "牌二": "Card Two",
    "牌三": "Card Three",
    "过去": "Past",
    "现在": "Present",
    "未来": "Future",
}

def _keyword(meaning: str) -> str:
    return meaning.split("、")[0]


def _display_for(card_name: str, orientation: str) -> CardDisplay:
    data = FULL_DECK[card_name]
    meaning = data["upright"] if orientation == "upright" else data["reversed"]
    return CardDisplay(
        name_zh=data["name_zh"],
        name_en=data.get("name_en", ""),
        keyword=_keyword(meaning),
    )


def _get_spread(spread_key: str) -> dict:
    spread = load_spreads().get(spread_key)
    if not spread:
        raise HTTPException(status_code=404, detail=f"未知牌阵：{spread_key}")
    return spread


@app.get("/api/spreads", response_model=list[SpreadOut])
def get_spreads():
    return [
        SpreadOut(
            key=key,
            name=s["name"],
            card_count=s["card_count"],
            positions=s["positions"],
            logic=s["logic"],
            description=s["description"],
        )
        for key, s in load_spreads().items()
    ]


def _build_draw_response(cards: list[dict], spread: dict) -> DrawResponse:
    core = find_core_card(cards, logic=spread["logic"])
    return DrawResponse(
        cards=[CardOut(**c) for c in cards],
        core_card=CardOut(**core),
        positions=spread["positions"],
        display=[_display_for(c["card"], c["orientation"]) for c in cards],
    )


@app.post("/api/draw", response_model=DrawResponse)
def draw(req: DrawRequest):
    spread = _get_spread(req.spread_key)
    cards = draw_cards(spread["card_count"])
    return _build_draw_response(cards, spread)


@app.post("/api/interpret", response_model=InterpretResponse)
def interpret(req: InterpretRequest):
    spread = _get_spread(req.spread_key)

    cards = [c.model_dump() for c in req.cards]
    core_card = req.core_card.model_dump()

    interpretations: list[InterpretationItem] = []
    for raw_position, card_info in zip(spread["positions"], cards):
        position = POSITION_EN.get(raw_position, raw_position) if req.language == "en" else raw_position
        is_core = card_info["card"] == core_card["card"]
        card_detail = FULL_DECK[card_info["card"]]
        text = interpret_single_card(
            req.question,
            card_info,
            position,
            card_detail,
            is_core,
            language=req.language,
        )
        interpretations.append(
            InterpretationItem(position=position, card=card_info["card"], interpretation=text)
        )

    summary = synthesize_reading(
        req.question,
        [item.model_dump() for item in interpretations],
        cards,
        core_card,
        language=req.language,
    )

    return InterpretResponse(interpretations=interpretations, summary=summary)


@app.get("/api/deck", response_model=list[DeckCardOut])
def get_deck():
    return [
        DeckCardOut(card=key, name_zh=data["name_zh"], name_en=data.get("name_en", ""))
        for key, data in FULL_DECK.items()
    ]


@app.post("/api/vision/recognize", response_model=VisionRecognizeResponse)
async def vision_recognize(file: UploadFile = File(...), expected_count: Optional[int] = Form(None)):
    image_bytes = await file.read()
    result = recognize_cards(image_bytes, expected_count=expected_count)
    return VisionRecognizeResponse(
        success=result["success"],
        cards=[
            VisionCardOut(
                card=c["card"],
                orientation=c["orientation"],
                confidence=c["confidence"],
                valid=c["valid"],
            )
            for c in result["cards"]
        ],
        error=result.get("error"),
    )


@app.post("/api/vision/resolve", response_model=DrawResponse)
def vision_resolve(req: ResolveRequest):
    spread = _get_spread(req.spread_key)
    cards = [c.model_dump() for c in req.cards]
    return _build_draw_response(cards, spread)


@app.post("/api/analytics/event", response_model=AcceptedResponse)
def record_usage_event(req: UsageEventRequest):
    try:
        insert_row(
            "usage_events",
            {
                "anonymous_id_hash": anonymous_hash(req.anonymous_id),
                "session_id_hash": anonymous_hash(req.session_id),
                "event_name": req.event,
                "spread_key": req.spread_key,
                "reading_mode": req.mode,
                "language": req.language,
                "reading_id_hash": anonymous_hash(req.client_reading_id) if req.client_reading_id else None,
            },
        )
    except TelemetryUnavailable as exc:
        raise HTTPException(status_code=503, detail="统计服务暂时不可用") from exc
    return AcceptedResponse(accepted=True)


@app.post("/api/analytics/feedback", response_model=AcceptedResponse)
def record_feedback(req: FeedbackRequest):
    try:
        insert_row(
            "reading_feedback",
            {
                "anonymous_id_hash": anonymous_hash(req.anonymous_id),
                "session_id_hash": anonymous_hash(req.session_id),
                "reading_id_hash": anonymous_hash(req.client_reading_id),
                "rating": req.rating,
                "comment": req.comment,
                "spread_key": req.spread_key,
                "reading_mode": req.mode,
                "language": req.language,
            },
        )
    except TelemetryUnavailable as exc:
        raise HTTPException(status_code=503, detail="反馈服务暂时不可用") from exc
    return AcceptedResponse(accepted=True)
