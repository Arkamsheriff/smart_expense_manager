import { useState } from 'react';
import { PageHeader } from '@/layouts/AppLayout';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { StatCard } from '@/components/ui/StatCard';
import { CategoryBadge } from '@/components/ui/Badge';
import { CardSkeleton, TableSkeleton } from '@/components/ui/Loading';
import { CategoryBarChart, MonthlySpendingLineChart } from '@/components/charts';
import { useAsync } from '@/hooks/useAsync';
import { reportsApi } from '@/api/reports';
import { formatCurrency, formatDateTime } from '@/utils/format';

type Period = 'today' | 'weekly' | 'monthly';

const PERIOD_LABEL: Record<Period, string> = {
  today: "Today's Expenses",
  weekly: "This Week's Expenses",
  monthly: "This Month's Expenses",
};

export function ReportsPage() {
  const [period, setPeriod] = useState<Period>('today');
  const [exporting, setExporting] = useState(false);
  const [exported, setExported] = useState(false);

  const { data: periodReport, loading: periodLoading } = useAsync(() => {
    if (period === 'today') return reportsApi.today();
    if (period === 'weekly') return reportsApi.weekly();
    return reportsApi.monthly();
  }, [period]);

  const { data: stats, loading: statsLoading } = useAsync(() => reportsApi.statistics());
  const { data: categorySummary, loading: categoryLoading } = useAsync(() => reportsApi.categorySummary());
  const { data: monthlySeries, loading: seriesLoading } = useAsync(() => reportsApi.monthlySeries());

  const handleExport = async () => {
    setExporting(true);
    setExported(false);
    try {
      await reportsApi.exportCsv();
      setExported(true);
    } finally {
      setExporting(false);
    }
  };

  return (
    <div>
      <PageHeader
        title="Reports"
        description="Spending breakdowns and trends"
        actions={
          <Button variant="secondary" onClick={handleExport} disabled={exporting}>
            {exporting ? 'Exporting…' : exported ? 'Exported ✓' : 'Export CSV'}
          </Button>
        }
      />

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {statsLoading || !stats ? (
          Array.from({ length: 4 }).map((_, i) => <CardSkeleton key={i} />)
        ) : (
          <>
            <StatCard label="Total Spending" value={formatCurrency(stats.total)} />
            <StatCard label="Average Expense" value={formatCurrency(stats.average)} />
            <StatCard label="Highest Expense" value={formatCurrency(stats.highest)} tone="rose" />
            <StatCard label="Lowest Expense" value={formatCurrency(stats.lowest)} tone="emerald" />
          </>
        )}
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <h2 className="text-base font-semibold">Spending by Category</h2>
          </CardHeader>
          <CardBody>
            {categoryLoading ? (
              <div className="py-10 text-center text-sm text-ink-soft">Loading…</div>
            ) : categorySummary && categorySummary.length > 0 ? (
              <CategoryBarChart data={categorySummary.map((c) => ({ category: c.category, total: c.total }))} />
            ) : (
              <p className="py-10 text-center text-sm text-ink-soft">No expense data yet.</p>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h2 className="text-base font-semibold">Monthly Spending Trend</h2>
          </CardHeader>
          <CardBody>
            {seriesLoading || !monthlySeries ? (
              <div className="py-10 text-center text-sm text-ink-soft">Loading…</div>
            ) : (
              <MonthlySpendingLineChart data={monthlySeries} />
            )}
          </CardBody>
        </Card>
      </div>

      <Card className="mb-6">
        <CardHeader>
          <h2 className="text-base font-semibold">Category Summary</h2>
        </CardHeader>
        {categoryLoading ? (
          <TableSkeleton rows={4} cols={4} />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-faint">
                  <th className="px-5 py-3 font-medium">Category</th>
                  <th className="px-5 py-3 text-right font-medium"># Expenses</th>
                  <th className="px-5 py-3 text-right font-medium">Total</th>
                  <th className="px-5 py-3 text-right font-medium">% of Spending</th>
                </tr>
              </thead>
              <tbody>
                {(categorySummary ?? []).map((c) => (
                  <tr key={c.category} className="border-b border-line last:border-0">
                    <td className="px-5 py-3.5">
                      <CategoryBadge category={c.category} />
                    </td>
                    <td className="num px-5 py-3.5 text-right text-ink-soft">{c.count}</td>
                    <td className="num px-5 py-3.5 text-right font-semibold">{formatCurrency(c.total)}</td>
                    <td className="num px-5 py-3.5 text-right text-ink-soft">{c.percentOfTotal}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <Card>
        <CardHeader>
          <h2 className="text-base font-semibold">{PERIOD_LABEL[period]}</h2>
          <div className="flex gap-1 rounded-md border border-line bg-paper p-1">
            {(['today', 'weekly', 'monthly'] as Period[]).map((p) => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={`focus-ring rounded px-3 py-1.5 text-xs font-medium transition-colors ${
                  period === p ? 'bg-white text-ink shadow-sm' : 'text-ink-soft hover:text-ink'
                }`}
              >
                {p === 'today' ? 'Today' : p === 'weekly' ? 'This Week' : 'This Month'}
              </button>
            ))}
          </div>
        </CardHeader>
        {periodLoading ? (
          <TableSkeleton rows={3} cols={3} />
        ) : !periodReport || periodReport.expenses.length === 0 ? (
          <p className="px-5 py-10 text-center text-sm text-ink-soft">No expenses in this period.</p>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-faint">
                    <th className="px-5 py-3 font-medium">Description</th>
                    <th className="px-5 py-3 font-medium">Category</th>
                    <th className="px-5 py-3 font-medium">Date</th>
                    <th className="px-5 py-3 text-right font-medium">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {periodReport.expenses.map((e) => (
                    <tr key={e.id} className="border-b border-line last:border-0">
                      <td className="px-5 py-3.5 font-medium">{e.description}</td>
                      <td className="px-5 py-3.5">
                        <CategoryBadge category={e.category} />
                      </td>
                      <td className="px-5 py-3.5 text-ink-soft">{formatDateTime(e.created_at)}</td>
                      <td className="num px-5 py-3.5 text-right font-semibold">{formatCurrency(e.amount)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="flex items-center justify-between border-t border-line px-5 py-3 text-sm">
              <span className="text-ink-soft">{periodReport.expenses.length} expenses</span>
              <span className="num font-semibold">Total: {formatCurrency(periodReport.total)}</span>
            </div>
          </>
        )}
      </Card>
    </div>
  );
}
