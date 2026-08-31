"use client";

import { useEffect, useRef, useState } from "react";
import { useLanguage } from "@/lib/language";

interface CardFanProps {
  totalPicks: number;
  onPick: () => void;
}

const SIGMA = 110;
const MAX_LIFT = 52;
const MAX_SCALE = 0.16;
const LERP = 0.22;

function getInitialLayout() {
  if (typeof window === "undefined") return { count: 21, deg: 78 };
  const small = window.innerWidth < 640;
  return small ? { count: 15, deg: 58 } : { count: 21, deg: 78 };
}

function getInitialReduceMotion() {
  if (typeof window === "undefined") return false;
  return matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export default function CardFan({ totalPicks, onPick }: CardFanProps) {
  const { language } = useLanguage();
  const stageRef = useRef<HTMLDivElement>(null);
  const lightRef = useRef<HTMLDivElement>(null);
  const cardRefs = useRef<(HTMLDivElement | null)[]>([]);
  const rafRef = useRef<number | null>(null);
  const pickedCueTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const touchClickResetTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pointerRef = useRef<{ x: number; y: number; active: boolean }>({ x: 0, y: 0, active: false });
  const hoverStateRef = useRef<Map<number, { lift: number; scale: number; bright: number }>>(new Map());
  const usedSetRef = useRef<Set<number>>(new Set());
  const touchInteractionRef = useRef(false);
  const candidateRef = useRef<number | null>(null);

  const [usedSet, setUsedSet] = useState<Set<number>>(new Set());
  const [reduceMotion] = useState(getInitialReduceMotion);
  const [layout] = useState(getInitialLayout);
  const [isHovering, setIsHovering] = useState(false);
  const [candidateIndex, setCandidateIndex] = useState<number | null>(null);
  const [lastPickedIndex, setLastPickedIndex] = useState<number | null>(null);

  const { count, deg } = layout;

  useEffect(() => {
    usedSetRef.current = usedSet;
  }, [usedSet]);

  function baseTransform(i: number) {
    const t = count === 1 ? 0.5 : i / (count - 1);
    const angle = (t - 0.5) * deg;
    return { angle, base: `translateX(-50%) rotate(${angle}deg)` };
  }

  function applyCardTransform(i: number, lift: number, scale: number, bright: number) {
    const el = cardRefs.current[i];
    if (!el || usedSetRef.current.has(i)) return;
    const { base } = baseTransform(i);
    el.style.transform = `${base} translateY(${-lift}px) scale(${scale})`;
    el.style.filter = bright > 0.01 ? `brightness(${1 + 0.38 * bright})` : "";
    el.style.zIndex = String(100 + Math.round(bright * 100));
    el.style.boxShadow =
      bright > 0.35
        ? `0 ${8 + 14 * bright}px ${24 + 20 * bright}px rgba(169,121,58,${0.18 + 0.22 * bright})`
        : "";
  }

  function resetCard(i: number) {
    const el = cardRefs.current[i];
    if (!el || usedSetRef.current.has(i)) return;
    const { base } = baseTransform(i);
    el.style.transform = base;
    el.style.filter = "";
    el.style.zIndex = String(i);
    el.style.boxShadow = "";
    hoverStateRef.current.delete(i);
  }

  function runHoverFrame() {
    rafRef.current = null;
    if (reduceMotion || !stageRef.current) return;

    const { x: clientX, active } = pointerRef.current;
    const rect = stageRef.current.getBoundingClientRect();

    if (lightRef.current) {
      lightRef.current.style.left = `${clientX - rect.left}px`;
      lightRef.current.style.top = `${pointerRef.current.y - rect.top}px`;
      lightRef.current.style.opacity = active ? "1" : "0";
    }

    let needsNextFrame = active;

    cardRefs.current.forEach((el, i) => {
      if (!el || usedSetRef.current.has(i)) return;

      let targetLift = 0;
      let targetScale = 1;
      let targetBright = 0;

      if (active) {
        const r = el.getBoundingClientRect();
        const cx = r.left + r.width / 2;
        const d = clientX - cx;
        const f = Math.exp(-(d * d) / (2 * SIGMA * SIGMA));
        targetLift = MAX_LIFT * f;
        targetScale = 1 + MAX_SCALE * f;
        targetBright = f;
      }

      const prev = hoverStateRef.current.get(i) ?? { lift: 0, scale: 1, bright: 0 };
      const lift = prev.lift + (targetLift - prev.lift) * LERP;
      const scale = prev.scale + (targetScale - prev.scale) * LERP;
      const bright = prev.bright + (targetBright - prev.bright) * LERP;

      hoverStateRef.current.set(i, { lift, scale, bright });
      applyCardTransform(i, lift, scale, bright);

      if (active || lift > 0.5 || scale > 1.005 || bright > 0.01) {
        needsNextFrame = true;
      }
    });

    if (needsNextFrame) {
      rafRef.current = requestAnimationFrame(runHoverFrame);
    }
  }

  function scheduleHoverFrame() {
    if (rafRef.current === null) {
      rafRef.current = requestAnimationFrame(runHoverFrame);
    }
  }

  useEffect(() => {
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
      if (pickedCueTimerRef.current !== null) clearTimeout(pickedCueTimerRef.current);
      if (touchClickResetTimerRef.current !== null) clearTimeout(touchClickResetTimerRef.current);
    };
  }, []);

  function handleMove(clientX: number, clientY: number) {
    if (reduceMotion) return;
    pointerRef.current = { x: clientX, y: clientY, active: true };
    setIsHovering(true);
    scheduleHoverFrame();
  }

  function resetHover() {
    pointerRef.current.active = false;
    setIsHovering(false);
    if (reduceMotion) return;
    scheduleHoverFrame();

    const settle = () => {
      let stillMoving = false;
      hoverStateRef.current.forEach((s, i) => {
        if (usedSetRef.current.has(i)) return;
        if (s.lift > 0.3 || s.bright > 0.02) stillMoving = true;
      });
      if (stillMoving) {
        scheduleHoverFrame();
        requestAnimationFrame(settle);
      } else {
        cardRefs.current.forEach((_, i) => resetCard(i));
      }
    };
    requestAnimationFrame(settle);
  }

  function nearestAvailableCard(clientX: number) {
    let nearest: number | null = null;
    let nearestDistance = Number.POSITIVE_INFINITY;

    cardRefs.current.forEach((card, index) => {
      if (!card || usedSetRef.current.has(index)) return;
      const rect = card.getBoundingClientRect();
      const distance = Math.abs(clientX - (rect.left + rect.width / 2));
      if (distance < nearestDistance) {
        nearest = index;
        nearestDistance = distance;
      }
    });

    return nearest;
  }

  function updateTouchCandidate(clientX: number, clientY: number) {
    touchInteractionRef.current = true;
    const nearest = nearestAvailableCard(clientX);
    candidateRef.current = nearest;
    setCandidateIndex(nearest);
    pointerRef.current = { x: clientX, y: clientY, active: true };
    setIsHovering(true);
    if (!reduceMotion) scheduleHoverFrame();
  }

  function finishTouchSelection(clientX?: number) {
    const nearest = clientX === undefined ? candidateRef.current : nearestAvailableCard(clientX);
    if (nearest !== null) {
      pick(nearest);
      if (typeof navigator !== "undefined" && "vibrate" in navigator) navigator.vibrate(12);
    }
    candidateRef.current = null;
    setCandidateIndex(null);
    resetHover();
    if (touchClickResetTimerRef.current !== null) clearTimeout(touchClickResetTimerRef.current);
    touchClickResetTimerRef.current = setTimeout(() => {
      touchInteractionRef.current = false;
    }, 520);
  }

  function pick(i: number) {
    if (usedSetRef.current.has(i) || usedSetRef.current.size >= totalPicks) return;
    const next = new Set(usedSetRef.current).add(i);
    usedSetRef.current = next;
    setUsedSet(next);
    setLastPickedIndex(i);
    if (pickedCueTimerRef.current !== null) clearTimeout(pickedCueTimerRef.current);
    pickedCueTimerRef.current = setTimeout(() => setLastPickedIndex(null), 620);
    onPick();
  }

  return (
    <div
      className="stage"
      ref={stageRef}
      onMouseMove={(e) => handleMove(e.clientX, e.clientY)}
      onMouseLeave={resetHover}
      onTouchStart={(e) => {
        const touch = e.touches[0];
        if (touch) updateTouchCandidate(touch.clientX, touch.clientY);
      }}
      onTouchMove={(e) => {
        e.preventDefault();
        const touch = e.touches[0];
        if (touch) updateTouchCandidate(touch.clientX, touch.clientY);
      }}
      onTouchEnd={(e) => finishTouchSelection(e.changedTouches[0]?.clientX)}
      onTouchCancel={() => {
        candidateRef.current = null;
        setCandidateIndex(null);
        resetHover();
      }}
    >
      <div className="cursor-light" ref={lightRef} />
      <div className="fan">
        {Array.from({ length: count }).map((_, i) => {
          const { base } = baseTransform(i);
          const used = usedSet.has(i);
          const cardClass = [
            "card",
            "cardback",
            !used && isHovering ? "hovered" : "",
            !used ? "fan-enter" : "",
            candidateIndex === i ? "touch-candidate" : "",
            lastPickedIndex === i ? "just-picked" : "",
          ]
            .filter(Boolean)
            .join(" ");

          return (
            <div
              key={i}
              ref={(el) => {
                cardRefs.current[i] = el;
              }}
              className={cardClass}
              tabIndex={0}
              role="button"
              aria-label={language === "zh" ? "选择这张牌" : "Select this card"}
              style={
                used
                  ? {
                      transform: "translateX(-50%) translateY(-160px) scale(1.1)",
                      opacity: 0,
                      pointerEvents: "none",
                      transition: "transform 0.65s cubic-bezier(0.16,1,0.3,1) 0.1s, opacity 0.45s ease 0.16s",
                      zIndex: i,
                    }
                  : {
                      transform: base,
                      zIndex: i,
                      animationDelay: `${i * 18}ms`,
                    }
              }
              onClick={() => {
                if (!touchInteractionRef.current) pick(i);
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  pick(i);
                }
              }}
            >
              <span className="touch-choice-label" aria-hidden="true">
                {language === "zh" ? "松开选中" : "Release to choose"}
              </span>
              <span className="sr-only">{language === "zh" ? "选择这张牌" : "Select this card"}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
