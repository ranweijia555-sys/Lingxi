"use client";

import { useLanguage } from "@/lib/language";

export default function SiteFooter() {
  const { language } = useLanguage();
  return (
    <footer className="site-footer">
      <span>ARCANA BOTANICA</span>
      <span className="footer-star" aria-hidden="true">✦</span>
      <span>{language === "zh" ? "循着直觉，阅读此刻" : "A quiet reflection for this moment"}</span>
    </footer>
  );
}
