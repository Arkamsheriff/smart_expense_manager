import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  LineChart,
  Line,
  Legend,
} from 'recharts';
import { formatCurrency } from '@/utils/format';

const COLORS = ['#0B6E4F', '#A6394A', '#9C6B0B', '#3B6FA6', '#6D4B9C', '#5B6472'];

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-md border border-line bg-surface px-3 py-2 text-xs shadow-card">
      {label && <div className="mb-1 font-medium text-ink">{label}</div>}
      {payload.map((p: any, i: number) => (
        <div key={i} className="flex items-center gap-1.5 text-ink-soft">
          <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: p.color ?? p.fill }} />
          {p.name}: <span className="num font-medium text-ink">{formatCurrency(p.value)}</span>
        </div>
      ))}
    </div>
  );
}

export function CategoryPieChart({ data }: { data: { category: string; total: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie data={data} dataKey="total" nameKey="category" cx="50%" cy="50%" innerRadius={55} outerRadius={90} paddingAngle={2}>
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend
          verticalAlign="bottom"
          height={36}
          formatter={(value) => <span className="text-xs text-ink-soft">{value}</span>}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function IncomeExpenseBarChart({ data }: { data: { month: string; income: number; expenses: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data} barGap={4}>
        <CartesianGrid stroke="#E1E3DD" vertical={false} />
        <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#4B5563' }} axisLine={{ stroke: '#E1E3DD' }} tickLine={false} />
        <YAxis tick={{ fontSize: 12, fill: '#4B5563' }} axisLine={false} tickLine={false} width={40} />
        <Tooltip content={<CustomTooltip />} />
        <Legend formatter={(value) => <span className="text-xs text-ink-soft">{value}</span>} />
        <Bar dataKey="income" name="Income" fill="#0B6E4F" radius={[4, 4, 0, 0]} />
        <Bar dataKey="expenses" name="Expenses" fill="#A6394A" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function MonthlySpendingLineChart({ data }: { data: { month: string; total: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={data}>
        <CartesianGrid stroke="#E1E3DD" vertical={false} />
        <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#4B5563' }} axisLine={{ stroke: '#E1E3DD' }} tickLine={false} />
        <YAxis tick={{ fontSize: 12, fill: '#4B5563' }} axisLine={false} tickLine={false} width={40} />
        <Tooltip content={<CustomTooltip />} />
        <Line type="monotone" dataKey="total" name="Spending" stroke="#0B6E4F" strokeWidth={2} dot={{ r: 3 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function CategoryBarChart({ data }: { data: { category: string; total: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data} layout="vertical" margin={{ left: 10 }}>
        <CartesianGrid stroke="#E1E3DD" horizontal={false} />
        <XAxis type="number" tick={{ fontSize: 12, fill: '#4B5563' }} axisLine={false} tickLine={false} />
        <YAxis type="category" dataKey="category" tick={{ fontSize: 12, fill: '#4B5563' }} axisLine={false} tickLine={false} width={90} />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey="total" name="Spent" fill="#0B6E4F" radius={[0, 4, 4, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
