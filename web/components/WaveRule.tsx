export default function WaveRule({ className }: { className?: string }) {
  return (
    <svg
      className={className ? `wave-rule ${className}` : "wave-rule"}
      viewBox="0 0 200 16"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M0 8 C 12 0, 22 16, 34 8 S 56 0, 68 8 S 90 16, 102 8 S 124 0, 136 8 S 158 16, 170 8 S 192 0, 200 8"
        stroke="currentColor"
        strokeWidth="1"
        opacity="0.6"
      />
      <circle cx="100" cy="8" r="2.4" fill="currentColor" opacity="0.75" />
    </svg>
  );
}
