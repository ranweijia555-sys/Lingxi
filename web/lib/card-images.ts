const NUMERAL_TO_DIGIT: Record<string, string> = {
  二: "2",
  三: "3",
  四: "4",
  五: "5",
  六: "6",
  七: "7",
  八: "8",
  九: "9",
  十: "10",
};

const CARD_ALIASES: Record<string, string> = {
  愚人: "愚者",
  女皇: "皇后",
  死神: "死亡",
  塔: "高塔",
  隐者: "隐士",
  "权杖Ace 一": "权杖手牌",
  "圣杯Ace 一": "圣杯手牌",
  "宝剑Ace 一": "宝剑首牌",
  "星币Ace 一": "星币首牌",
};

export function cardImagePath(nameZh: string) {
  const normalized = nameZh.trim();
  const aliased = CARD_ALIASES[normalized] ?? normalized.replace("王后", "女王");
  const numberedMinor = aliased.match(/^(权杖|圣杯|宝剑|星币)([二三四五六七八九十])$/);
  const filename = numberedMinor
    ? `${numberedMinor[1]}${NUMERAL_TO_DIGIT[numberedMinor[2]]}`
    : aliased;

  return encodeURI(`/cards/${filename}.webp`);
}

export const CARD_BACK_PATH = encodeURI("/cards/牌背.webp");
