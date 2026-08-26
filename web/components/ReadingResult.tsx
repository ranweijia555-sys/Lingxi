"use client";

import { useState } from "react";

import {
  submitReadingFeedback,
  type FeedbackRating,
  type ReadingMode,
} from "@/lib/analytics";
import { localizedCardKey, useLanguage } from "@/lib/language";
import type { InterpretResponse } from "@/lib/types";

export default function ReadingResult({
  result,
  readingId,
  spreadKey,
  mode,
}: {
  result: InterpretResponse;
  readingId: string;
  spreadKey: string;
  mode: ReadingMode;
}) {
  const { language } = useLanguage();
  const [rating, setRating] = useState<FeedbackRating | null>(null);
  const [comment, setComment] = useState("");
  const [feedbackState, setFeedbackState] = useState<"idle" | "sending" | "sent" | "error">("idle");
  const copy = language === "zh" ? {
    privateArchive: "此次占卜仅保存在此浏览器的私人档案中",
    feedbackTitle: "这次解读对你有帮助吗？",
    feedbackNote: "反馈会匿名发送；你的问题、牌面与解读不会上传。",
    helpful: "有帮助",
    neutral: "一般",
    notHelpful: "没有帮助",
    placeholder: "可选：告诉我哪里可以做得更好（最多 500 字）",
    submit: "提交反馈",
    sending: "正在提交…",
    sent: "谢谢，你的反馈已经匿名记录。",
    error: "暂时无法提交，请稍后再试。",
  } : {
    privateArchive: "This reading is saved only in this browser's private archive",
    feedbackTitle: "Was this reading helpful?",
    feedbackNote: "Feedback is anonymous. Your question, cards, and reading are never uploaded with it.",
    helpful: "Helpful",
    neutral: "Neutral",
    notHelpful: "Not helpful",
    placeholder: "Optional: tell us what could be better (500 characters max)",
    submit: "Send feedback",
    sending: "Sending…",
    sent: "Thank you. Your anonymous feedback has been recorded.",
    error: "Feedback could not be sent. Please try again later.",
  };

  async function handleFeedbackSubmit() {
    if (!rating || feedbackState === "sending" || feedbackState === "sent") return;
    setFeedbackState("sending");
    try {
      await submitReadingFeedback({
        rating,
        comment,
        spreadKey,
        mode,
        language,
        readingId,
      });
      setFeedbackState("sent");
    } catch {
      setFeedbackState("error");
    }
  }

  return (
    <div className="reading-result">
      <header className="result-heading">
        <span className="eyebrow">YOUR READING</span>
        <h2>{language === "zh" ? "牌面给出的回应" : "What the cards reflect"}</h2>
        <p>{language === "zh" ? "每一张牌先回应它所在的位置，最后再汇成完整的线索。" : "Each card speaks from its position before the reading comes together as a whole."}</p>
      </header>
      <div className="interpretation-list">
        {result.interpretations.map((item, i) => (
          <article className="interp-block" key={i}>
            <span className="interp-index">{String(i + 1).padStart(2, "0")}</span>
            <div>
              <div className="interp-title">
                <span>{item.position}</span>
                <strong>{localizedCardKey(item.card, language)}</strong>
              </div>
              <p>{item.interpretation}</p>
            </div>
          </article>
        ))}
      </div>
      <div className="summary-block">
        <span className="eyebrow">SYNTHESIS</span>
        <h3>{language === "zh" ? "综合启示" : "Synthesis"}</h3>
        <p>{result.summary}</p>
        <div className="summary-mark" aria-hidden="true">✦</div>
      </div>
      <p className="reading-id">
        <span aria-hidden="true">◇</span> {copy.privateArchive}
      </p>
      <section className="reading-feedback" aria-labelledby="feedback-title">
        <span className="eyebrow">FEEDBACK</span>
        <h3 id="feedback-title">{copy.feedbackTitle}</h3>
        <p>{copy.feedbackNote}</p>
        {feedbackState === "sent" ? (
          <p className="feedback-status success" role="status">{copy.sent}</p>
        ) : (
          <>
            <div className="feedback-rating" role="group" aria-label={copy.feedbackTitle}>
              {([
                ["helpful", copy.helpful, "↑"],
                ["neutral", copy.neutral, "◇"],
                ["not_helpful", copy.notHelpful, "↓"],
              ] as const).map(([value, label, icon]) => (
                <button
                  type="button"
                  key={value}
                  className={rating === value ? "selected" : ""}
                  aria-pressed={rating === value}
                  onClick={() => {
                    setRating(value);
                    if (feedbackState === "error") setFeedbackState("idle");
                  }}
                >
                  <span aria-hidden="true">{icon}</span>{label}
                </button>
              ))}
            </div>
            {rating && (
              <div className="feedback-detail">
                <textarea
                  value={comment}
                  maxLength={500}
                  onChange={(event) => setComment(event.target.value)}
                  placeholder={copy.placeholder}
                  aria-label={copy.placeholder}
                />
                <button
                  type="button"
                  className="primary feedback-submit"
                  disabled={feedbackState === "sending"}
                  onClick={handleFeedbackSubmit}
                >
                  {feedbackState === "sending" ? copy.sending : copy.submit} <span aria-hidden="true">✦</span>
                </button>
              </div>
            )}
            {feedbackState === "error" && <p className="feedback-status error" role="alert">{copy.error}</p>}
          </>
        )}
      </section>
    </div>
  );
}
