interface ProgressBarProps {
  percent: number;
  tone?: 'emerald' | 'amber' | 'rose';
}

export function ProgressBar({ percent, tone }: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(percent, 100));
  const resolvedTone = tone ?? (percent >= 100 ? 'rose' : percent >= 80 ? 'amber' : 'emerald');
  const barClass = {
    emerald: 'bg-emerald-500',
    amber: 'bg-amber-500',
    rose: 'bg-rose-500',
  }[resolvedTone];

  return (
    <div className="h-2 w-full rounded-full bg-ink/[0.06]" role="progressbar" aria-valuenow={clamped} aria-valuemin={0} aria-valuemax={100}>
      <div className={`h-2 rounded-full ${barClass} transition-all`} style={{ width: `${clamped}%` }} />
    </div>
  );
}
