import { Link } from 'react-router-dom';
import { PageHeader } from '@/layouts/AppLayout';
import { StatCard } from '@/components/ui/StatCard';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { CardSkeleton } from '@/components/ui/Loading';
import { CategoryBadge } from '@/components/ui/Badge';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { CategoryPieChart, IncomeExpenseBarChart } from '@/components/charts';
import { useAsync } from '@/hooks/useAsync';
import { dashboardApi } from '@/api/reports';
import { formatCurrency, formatDate, formatPercent } from '@/utils/format';

export function DashboardPage() {
  const { data, loading, error } = useAsync(() => dashboardApi.summary());

  if (loading) {
    return (
      <div>
        <PageHeader title="Dashboard" description="Your financial overview" />
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div>
        <PageHeader title="Dashboard" />
        <p className="text-sm text-rose-500">Couldn't load dashboard data: {error}</p>
      </div>
    );
  }

  return (
    <div>
      <PageHeader title="Dashboard" description="Your financial overview" />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Total Income" value={formatCurrency(data.totalIncome)} tone="emerald" />
        <StatCard label="Total Expenses" value={formatCurrency(data.totalExpenses)} tone="rose" />
        <StatCard
          label="Current Balance"
          value={formatCurrency(data.currentBalance)}
          tone={data.currentBalance >= 0 ? 'emerald' : 'rose'}
        />
        <StatCard label="Savings Rate" value={formatPercent(data.savingsRate)} />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader>
            <h2 className="text-base font-semibold">Income vs Expenses</h2>
          </CardHeader>
          <CardBody>
            <IncomeExpenseBarChart data={data.incomeVsExpenseByMonth} />
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h2 className="text-base font-semibold">Spending by Category</h2>
          </CardHeader>
          <CardBody>
            {data.expenseByCategory.length ? (
              <CategoryPieChart data={data.expenseByCategory} />
            ) : (
              <p className="py-10 text-center text-sm text-ink-soft">No expense data yet.</p>
            )}
          </CardBody>
        </Card>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <h2 className="text-base font-semibold">Recent Expenses</h2>
            <Link to="/expenses" className="text-xs font-medium text-emerald-600 hover:underline">
              View all
            </Link>
          </CardHeader>
          <div>
            {data.recentExpenses.length === 0 ? (
              <p className="px-5 py-8 text-center text-sm text-ink-soft">No expenses recorded yet.</p>
            ) : (
              data.recentExpenses.map((e) => (
                <div key={e.id} className="flex items-center justify-between border-b border-line px-5 py-3 last:border-0">
                  <div>
                    <div className="text-sm font-medium">{e.description}</div>
                    <div className="mt-0.5 flex items-center gap-2">
                      <CategoryBadge category={e.category} />
                      <span className="text-xs text-ink-faint">{formatDate(e.created_at)}</span>
                    </div>
                  </div>
                  <span className="num text-sm font-semibold text-rose-500">-{formatCurrency(e.amount)}</span>
                </div>
              ))
            )}
          </div>
        </Card>

        <Card>
          <CardHeader>
            <h2 className="text-base font-semibold">Recent Income</h2>
            <Link to="/income" className="text-xs font-medium text-emerald-600 hover:underline">
              View all
            </Link>
          </CardHeader>
          <div>
            {data.recentIncome.length === 0 ? (
              <p className="px-5 py-8 text-center text-sm text-ink-soft">No income recorded yet.</p>
            ) : (
              data.recentIncome.map((i) => (
                <div key={i.id} className="flex items-center justify-between border-b border-line px-5 py-3 last:border-0">
                  <div>
                    <div className="text-sm font-medium">{i.source}</div>
                    <div className="mt-0.5 flex items-center gap-2">
                      <CategoryBadge category={i.category} />
                      <span className="text-xs text-ink-faint">{formatDate(i.received_at)}</span>
                    </div>
                  </div>
                  <span className="num text-sm font-semibold text-emerald-600">+{formatCurrency(i.amount)}</span>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <h2 className="text-base font-semibold">Budget Usage</h2>
            <Link to="/budgets" className="text-xs font-medium text-emerald-600 hover:underline">
              View all
            </Link>
          </CardHeader>
          <CardBody className="flex flex-col gap-4">
            {data.budgets.length === 0 ? (
              <p className="text-center text-sm text-ink-soft">No budgets set yet.</p>
            ) : (
              data.budgets.slice(0, 4).map((b) => (
                <div key={b.id}>
                  <div className="mb-1.5 flex items-center justify-between text-sm">
                    <span className="font-medium">{b.category}</span>
                    <span className="num text-ink-soft">
                      {formatCurrency(b.spent)} / {formatCurrency(b.amount)}
                    </span>
                  </div>
                  <ProgressBar percent={b.percentUsed} />
                </div>
              ))
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h2 className="text-base font-semibold">Goal Progress</h2>
            <Link to="/goals" className="text-xs font-medium text-emerald-600 hover:underline">
              View all
            </Link>
          </CardHeader>
          <CardBody className="flex flex-col gap-4">
            {data.goals.length === 0 ? (
              <p className="text-center text-sm text-ink-soft">No goals set yet.</p>
            ) : (
              data.goals.map((g) => (
                <div key={g.id}>
                  <div className="mb-1.5 flex items-center justify-between text-sm">
                    <span className="font-medium">{g.name}</span>
                    <span className="num text-ink-soft">{formatPercent(g.percentComplete)}</span>
                  </div>
                  <ProgressBar percent={g.percentComplete} tone="emerald" />
                </div>
              ))
            )}
          </CardBody>
        </Card>
      </div>

      <div className="mt-6">
        <Card>
          <CardHeader>
            <h2 className="text-base font-semibold">Upcoming Recurring Expenses</h2>
            <Link to="/recurring" className="text-xs font-medium text-emerald-600 hover:underline">
              View all
            </Link>
          </CardHeader>
          <div>
            {data.upcomingRecurring.length === 0 ? (
              <p className="px-5 py-8 text-center text-sm text-ink-soft">No active recurring expenses.</p>
            ) : (
              data.upcomingRecurring.map((r) => (
                <div key={r.id} className="flex items-center justify-between border-b border-line px-5 py-3 last:border-0">
                  <div>
                    <div className="text-sm font-medium">{r.description}</div>
                    <div className="mt-0.5 flex items-center gap-2">
                      <CategoryBadge category={r.category} />
                      <span className="text-xs text-ink-faint">Due {formatDate(r.next_due_date)}</span>
                    </div>
                  </div>
                  <span className="num text-sm font-semibold">{formatCurrency(r.amount)}</span>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
