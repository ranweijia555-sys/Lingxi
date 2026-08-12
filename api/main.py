"""灵案 AstRa - FastAPI 后端（供 Next.js 抽牌页调用，逻辑复用 tarot/ 包）"""
import os
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from tarot.analyzer import build_analysis_report
from tarot.data_loader import load_full_deck, load_spreads
from tarot.drawer import draw_cards, find_core_card
from tarot.history import load_history, save_reading
from tarot.interpreter import interpret_single_card, synthesize_reading
from tarot.vision import recognize_cards

from api.schemas import (
    CardDisplay,
    CardOut,
    DeckCardOut,
    DrawRequest,
    DrawResponse,
    HistoryEntry,
    InterpretationItem,
    InterpretRequest,
    InterpretResponse,
    ResolveRequest,
    SpreadOut,
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
    for position, card_info in zip(spread["positions"], cards):
        is_core = card_info["card"] == core_card["card"]
        card_detail = FULL_DECK[card_info["card"]]
        text = interpret_single_card(req.question, card_info, position, card_detail, is_core)
        interpretations.append(
            InterpretationItem(position=position, card=card_info["card"], interpretation=text)
        )

    analysis_report = build_analysis_report(cards, core_card)
    summary = synthesize_reading(
        req.question,
        [item.model_dump() for item in interpretations],
        analysis_report,
    )

    reading_id = save_reading(
        question=req.question,
        spread_name=spread["name"],
        cards=cards,
        core_card=core_card,
        single_interpretations=[item.model_dump() for item in interpretations],
        summary=summary,
    )

    return InterpretResponse(interpretations=interpretations, summary=summary, reading_id=reading_id)


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


@app.get("/api/history", response_model=list[HistoryEntry])
def get_history(limit: int = 20):
    history = load_history()
    recent = history[-limit:][::-1]
    return [HistoryEntry(**entry) for entry in recent]
