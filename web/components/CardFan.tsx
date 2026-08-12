"use client";

import { useEffect, useRef, useState } from "react";

interface CardFanProps {
  totalPicks: number;
  onPick: () => void;
}

const SIGMA = 90;
const MAX_LIFT = 46;
const MAX_SCALE = 0.14;

export default function CardFan({ totalPicks, onPick }: CardFanProps) {
  const stageRef = useRef<HTMLDivElement>(null);
  const lightRef = useRef<HTMLDivElement>(null);
  const cardRefs = useRef<(HTMLDivElement | null)[]>([]);
  const [usedSet, setUsedSet] = useState<Set<number>>(new Set());
  const [reduceMotion, setReduceMotion] = useState(false);
  const [layout, setLayout] = useState({ count: 21, deg: 78 });

  useEffect(() => {
    setReduceMotion(matchMedia("(prefers-reduced-motion: reduce)").matches);
    const small = window.innerWidth < 640;
    setLayout(small ? { count: 15, deg: 58 } : { count: 21, deg: 78 });
  }, []);

  const { count, deg } = layout;

  function baseTransform(i: number) {
    const t = count === 1 ? 0.5 : i / (count - 1);
    const angle = (t - 0.5) * deg;
    return { angle, base: `translateX(-50%) rotate(${angle}deg)` };
  }

  function handleMove(clientX: number, clientY: number) {
    if (reduceMotion || !stageRef.current) return;
    const rect = stageRef.current.getBoundingClientRect();
    if (lightRef.current) {
      lightRef.current.style.left = `${clientX - rect.left}px`;
      lightRef.current.style.top = `${clientY - rect.top}px`;
      lightRef.current.style.opacity = "1";
    }
    cardRefs.current.forEach((el, i) => {
      if (!el || usedSet.has(i)) return;
      const r = el.getBoundingClientRect();
      const cx = r.left + r.width / 2;
      const d = clientX - cx;
      const f = Math.exp(-(d * d) / (2 * SIGMA * SIGMA));
      const lift = MAX_LIFT * f;
      const scale = 1 + MAX_SCALE * f;
      const { base } = baseTransform(i);
      el.style.transform = `${base} translateY(${-lift}px) scale(${scale})`;
      el.style.filter = `brightness(${1 + 0.35 * f})`;
      el.style.zIndex = String(100 + Math.round(f * 100));
      el.style.boxShadow = f > 0.5 ? `0 12px 30px rgba(169,121,58,${0.28 * f})` : "";
    });
  }

  function resetHover() {
    if (reduceMotion) return;
    if (lightRef.current) lightRef.current.style.opacity = "0";
    cardRefs.current.forEach((el, i) => {
      if (!el || usedSet.has(i)) return;
      const { base } = baseTransform(i);
      el.style.transform = base;
      el.style.filter = "";
      el.style.zIndex = String(i);
      el.style.boxShadow = "";
    });
  }

  function pick(i: number) {
    if (usedSet.has(i) || usedSet.size >= totalPicks) return;
    setUsedSet((prev) => new Set(prev).add(i));
    onPick();
  }

  return (
    <div
      className="stage"
      ref={stageRef}
      onMouseMove={(e) => handleMove(e.clientX, e.clientY)}
      onMouseLeave={resetHover}
      onTouchMove={(e) => {
        const t = e.touches[0];
        if (t) handleMove(t.clientX, t.clientY);
      }}
    >
      <div className="cursor-light" ref={lightRef} />
      <div className="fan">
        {Array.from({ length: count }).map((_, i) => {
          const { base } = baseTransform(i);
          const used = usedSet.has(i);
          return (
            <div
              key={i}
              ref={(el) => {
                cardRefs.current[i] = el;
              }}
              className="card cardback"
              tabIndex={0}
              role="button"
              aria-label="一张牌"
              style={
                used
                  ? {
                      transform: "translateX(-50%) translateY(-160px) scale(1.1)",
                      opacity: 0,
                      pointerEvents: "none",
                      transition: "transform .5s cubic-bezier(.2,.8,.2,1), opacity .5s ease",
                      zIndex: i,
                    }
                  : { transform: base, zIndex: i }
              }
              onClick={() => pick(i)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  pick(i);
                }
              }}
            >
              <div className="ring" />
              <div className="sigil">✦</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
