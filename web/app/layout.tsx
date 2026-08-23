import type { Metadata } from "next";
import { Cormorant_Garamond, Inter } from "next/font/google";
import { LanguageProvider } from "@/lib/language";
import "./globals.css";

const serif = Cormorant_Garamond({
  variable: "--font-editorial",
  subsets: ["latin"],
  weight: ["500", "600"],
  style: ["normal", "italic"],
  display: "swap",
});

const sans = Inter({
  variable: "--font-interface",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "灵案 ASTRA · 静谧塔罗占卜",
  description: "以植物、星辰与直觉为线索的塔罗占卜体验。",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className={[serif.variable, sans.variable].join(" ")}>
        <LanguageProvider>{children}</LanguageProvider>
      </body>
    </html>
  );
}
