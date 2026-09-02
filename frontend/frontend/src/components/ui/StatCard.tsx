import { ReactNode } from 'react';
import { Card } from './Card';

interface StatCardProps {
  label: string;
  value: string;
  trend?: { direction: 'up' | 'down'; label: string };
  tone?: 'default' | 'emerald' | 'rose';
  icon?: ReactNode;
}

export function StatCard({ label, value, trend, tone = 'default', icon }: StatCardProps) {
  const valueColor = tone === 'emerald' ? 'text-emerald-600' : tone === 'rose' ? 'text-rose-500' : 'text-ink';

  return (
    <Card className="p-5">
      <div className="flex items-start justify-between">
        <span className="text-xs font-medium uppercase tracking-wide text-ink-faint">{label}</span>
        {icon && <span className="text-ink-faint">{icon}</span>}
      </div>
      <div className={`num mt-2 text-2xl font-semibold ${valueColor}`}>{value}</div>
      {trend && (
        <div className={`mt-1.5 text-xs font-medium ${trend.direction === 'up' ? 'text-emerald-600' : 'text-rose-500'}`}>
          {trend.direction === 'up' ? '↑' : '↓'} {trend.label}
        </div>
      )}
    </Card>
  );
}
