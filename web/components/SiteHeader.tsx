"use client";

import Link from "next/link";
import { useLanguage } from "@/lib/language";

export default function SiteHeader({ active = "reading" }: { active?: "reading" | "history" }) {
  const { language, setLanguage } = useLanguage();

  return (
    <nav className="site-nav" aria-label="主导航">
      <Link className="brand" href="/" aria-label="灵案首页">
        <span className="brand-sun" aria-hidden="true">✦</span>
        <span className="brand-copy">
          <strong>灵案</strong>
          <small>ASTRA TAROT</small>
        </span>
      </Link>
      <div className="nav-links">
        <Link className={active === "reading" ? "active" : ""} href="/">
          {language === "zh" ? "占卜" : "Reading"}
        </Link>
        <Link className={active === "history" ? "active" : ""} href="/history">
          {language === "zh" ? "档案" : "Archive"}
        </Link>
        <div className="language-switch" aria-label="Language">
          <button className={language === "zh" ? "active" : ""} onClick={() => setLanguage("zh")}>中</button>
          <span>/</span>
          <button className={language === "en" ? "active" : ""} onClick={() => setLanguage("en")}>EN</button>
        </div>
      </div>
    </nav>
  );
}
