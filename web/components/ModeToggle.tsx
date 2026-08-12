"use client";

export type ReadingMode = "draw" | "photo";

interface ModeToggleProps {
  mode: ReadingMode;
  onChange: (mode: ReadingMode) => void;
}

export default function ModeToggle({ mode, onChange }: ModeToggleProps) {
  return (
    <div className="mode-toggle">
      <button
        type="button"
        className={mode === "draw" ? "active" : ""}
        onClick={() => onChange("draw")}
      >
        🎴 系统为我抽牌
      </button>
      <button
        type="button"
        className={mode === "photo" ? "active" : ""}
        onClick={() => onChange("photo")}
      >
        📷 我拍照识别自己抽的牌
      </button>
    </div>
  );
}
