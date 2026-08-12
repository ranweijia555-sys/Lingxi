export default function CornerFlourish({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d="M2 46 C2 20 20 2 46 2" stroke="currentColor" strokeWidth="1" opacity="0.55" />
      <path d="M4 32 C12 28 17 22 19 12" stroke="currentColor" strokeWidth="1" opacity="0.45" />
      <circle cx="19" cy="12" r="2" fill="currentColor" opacity="0.55" />
    </svg>
  );
}
