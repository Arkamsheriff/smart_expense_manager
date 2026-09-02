import { PageHeader } from '@/layouts/AppLayout';
import { Card } from '@/components/ui/Card';

export function NetWorthPage() {
  return (
    <div>
      <PageHeader title="Net Worth" description="Track assets, liabilities, and overall net worth" />

      <Card className="flex flex-col items-center justify-center gap-4 px-6 py-20 text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-emerald-50 text-emerald-600">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
            <path
              d="M12 21c4.97 0 9-4.03 9-9s-4.03-9-9-9-9 4.03-9 9 4.03 9 9 9Zm0-13v8m-3-3 3 3 3-3"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div>
          <h2 className="font-display text-xl font-semibold">Net Worth Management</h2>
          <p className="mt-2 max-w-md text-sm text-ink-soft">
            Coming Soon. This page is reserved for tracking assets, liabilities, and net worth over time once that
            functionality is built into the backend.
          </p>
        </div>
        <span className="mt-1 inline-flex items-center gap-1.5 rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-600">
          <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
          Planned feature
        </span>
      </Card>
    </div>
  );
}
