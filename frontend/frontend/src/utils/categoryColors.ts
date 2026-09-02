// Deterministic color assignment per category name so badges stay consistent
// without a hardcoded map that goes stale as categories change.

const PALETTE = [
  { bg: 'bg-emerald-50', text: 'text-emerald-600', dot: 'bg-emerald-500' },
  { bg: 'bg-rose-50', text: 'text-rose-600', dot: 'bg-rose-500' },
  { bg: 'bg-amber-50', text: 'text-amber-600', dot: 'bg-amber-500' },
  { bg: 'bg-sky-50', text: 'text-sky-600', dot: 'bg-sky-500' },
  { bg: 'bg-violet-50', text: 'text-violet-600', dot: 'bg-violet-500' },
  { bg: 'bg-lime-50', text: 'text-lime-700', dot: 'bg-lime-600' },
];

function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

export function categoryStyle(category: string) {
  const idx = hashString(category) % PALETTE.length;
  return PALETTE[idx];
}
