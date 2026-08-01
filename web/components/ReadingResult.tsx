import type { InterpretResponse } from "@/lib/types";

export default function ReadingResult({ result }: { result: InterpretResponse }) {
  return (
    <div className="reading-result">
      <h3>✦ 逐张深度解读</h3>
      {result.interpretations.map((item, i) => (
        <div className="interp-block" key={i}>
          <div className="interp-title">
            {item.position} · {item.card}
          </div>
          <p>{item.interpretation}</p>
        </div>
      ))}
      <div className="summary-block">
        <p>{result.summary}</p>
      </div>
      <p className="reading-id">📜 已保存为占卜 #{result.reading_id}</p>
    </div>
  );
}
