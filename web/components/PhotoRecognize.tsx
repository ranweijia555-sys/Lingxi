"use client";

import { useState } from "react";

import { getDeck, recognizeCards } from "@/lib/api";
import type { DeckCard, DrawnCard, Orientation, VisionCard } from "@/lib/types";

interface PhotoRecognizeProps {
  expectedCount: number;
  onConfirm: (cards: DrawnCard[]) => void;
}

export default function PhotoRecognize({ expectedCount, onConfirm }: PhotoRecognizeProps) {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [recognizing, setRecognizing] = useState(false);
  const [recognized, setRecognized] = useState<VisionCard[] | null>(null);
  const [deck, setDeck] = useState<DeckCard[] | null>(null);
  const [corrections, setCorrections] = useState<DrawnCard[]>([]);
  const [error, setError] = useState<string | null>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setPreviewUrl(URL.createObjectURL(f));
    setRecognized(null);
    setError(null);
  }

  async function handleRecognize() {
    if (!file) return;
    setRecognizing(true);
    setError(null);
    try {
      const [res, deckList] = await Promise.all([
        recognizeCards(file, expectedCount),
        deck ?? getDeck(),
      ]);
      if (!deck) setDeck(deckList);
      if (res.success && res.cards.length) {
        setRecognized(res.cards);
        setCorrections(res.cards.map((c) => ({ card: c.card, orientation: c.orientation })));
      } else {
        setError(res.error || "识别失败，请换一张更清晰的照片，或改用系统抽牌");
      }
    } catch {
      setError("识别失败，请稍后重试");
    } finally {
      setRecognizing(false);
    }
  }

  function updateCorrection(index: number, patch: Partial<DrawnCard>) {
    setCorrections((prev) => prev.map((c, i) => (i === index ? { ...c, ...patch } : c)));
  }

  return (
    <div className="photo-recognize">
      <label className="field-label" htmlFor="photo-input">
        上传你抽的牌的照片（清晰平铺最佳）
      </label>
      <input id="photo-input" type="file" accept="image/jpeg,image/png,image/jpg" onChange={handleFileChange} />

      {previewUrl && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={previewUrl} alt="你上传的照片" className="photo-preview" />
      )}

      {file && !recognized && (
        <button className="primary" onClick={handleRecognize} disabled={recognizing}>
          {recognizing ? "🔍 AI 正在识别牌面…" : "🔍 识别这些牌"}
        </button>
      )}

      {error && <p className="error">{error}</p>}

      {recognized && deck && (
        <div className="correction-form">
          <p className="field-label">✍️ 确认 / 修正识别结果</p>
          {recognized.map((c, i) => {
            const currentName = deck.find((d) => d.card === corrections[i]?.card)?.name_zh ?? "";
            const currentOrientation = corrections[i]?.orientation;
            return (
              <div className="correction-row" key={i}>
                <div className="correction-header">
                  <span className="correction-label">
                    第 {i + 1} 张{c.confidence < 0.7 ? "　⚠️ 置信度低" : ""}
                  </span>
                  <span className="correction-preview">
                    {currentName}　{currentOrientation === "upright" ? "正位" : "逆位"}
                  </span>
                </div>
                <div className="correction-fields">
                  <select
                    className="correction-card-select"
                    value={corrections[i]?.card}
                    onChange={(e) => updateCorrection(i, { card: e.target.value })}
                  >
                    {deck.map((d) => (
                      <option key={d.card} value={d.card}>
                        {d.name_zh}
                      </option>
                    ))}
                  </select>
                  <select
                    className="correction-orientation"
                    value={corrections[i]?.orientation}
                    onChange={(e) => updateCorrection(i, { orientation: e.target.value as Orientation })}
                  >
                    <option value="upright">正位</option>
                    <option value="reversed">逆位</option>
                  </select>
                </div>
              </div>
            );
          })}
          <button className="primary" onClick={() => onConfirm(corrections)}>
            ✦ 开始解读 ✦
          </button>
        </div>
      )}
    </div>
  );
}
