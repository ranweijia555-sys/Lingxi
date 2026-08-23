"use client";

import { useState } from "react";

import { getDeck, recognizeCards } from "@/lib/api";
import { useLanguage } from "@/lib/language";
import type { DeckCard, DrawnCard, Orientation, VisionCard } from "@/lib/types";

interface PhotoRecognizeProps {
  expectedCount: number;
  onConfirm: (cards: DrawnCard[]) => void;
}

export default function PhotoRecognize({ expectedCount, onConfirm }: PhotoRecognizeProps) {
  const { language } = useLanguage();
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
        <span>03</span> {language === "zh" ? "上传牌面照片" : "Upload a card photo"}
      </label>
      <label className="file-drop" htmlFor="photo-input">
        <span className="file-drop-icon" aria-hidden="true">＋</span>
        <strong>{file ? file.name : language === "zh" ? "选择一张照片" : "Choose a photo"}</strong>
        <small>{language === "zh" ? "JPG 或 PNG · 清晰平铺效果最佳" : "JPG or PNG · A clear flat layout works best"}</small>
      </label>
      <input className="sr-only" id="photo-input" type="file" accept="image/jpeg,image/png,image/jpg" onChange={handleFileChange} />

      {previewUrl && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={previewUrl} alt="你上传的照片" className="photo-preview" />
      )}

      {file && !recognized && (
        <button className="primary" onClick={handleRecognize} disabled={recognizing}>
          {recognizing ? (language === "zh" ? "正在辨认牌面…" : "Recognizing cards…") : (language === "zh" ? "识别这些牌" : "Recognize cards")}
        </button>
      )}

      {error && <p className="error">{error}</p>}

      {recognized && deck && (
        <div className="correction-form">
          <p className="field-label"><span>04</span> {language === "zh" ? "确认识别结果" : "Confirm the result"}</p>
          {recognized.map((c, i) => {
            const currentCard = deck.find((d) => d.card === corrections[i]?.card);
            const currentName = language === "zh" ? currentCard?.name_zh ?? "" : currentCard?.name_en ?? "";
            const currentOrientation = corrections[i]?.orientation;
            return (
              <div className="correction-row" key={i}>
                <div className="correction-header">
                  <span className="correction-label">
                    {language === "zh" ? `第 ${i + 1} 张` : `Card ${i + 1}`}{c.confidence < 0.7 ? (language === "zh" ? " · 建议确认" : " · Please check") : ""}
                  </span>
                  <span className="correction-preview">
                    {currentName}　{currentOrientation === "upright" ? (language === "zh" ? "正位" : "Upright") : (language === "zh" ? "逆位" : "Reversed")}
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
                        {language === "zh" ? d.name_zh : d.name_en}
                      </option>
                    ))}
                  </select>
                  <select
                    className="correction-orientation"
                    value={corrections[i]?.orientation}
                    onChange={(e) => updateCorrection(i, { orientation: e.target.value as Orientation })}
                  >
                    <option value="upright">{language === "zh" ? "正位" : "Upright"}</option>
                    <option value="reversed">{language === "zh" ? "逆位" : "Reversed"}</option>
                  </select>
                </div>
              </div>
            );
          })}
          <button className="primary" onClick={() => onConfirm(corrections)}>
            {language === "zh" ? "开始解读" : "Begin interpretation"} <span aria-hidden="true">✦</span>
          </button>
        </div>
      )}
    </div>
  );
}
