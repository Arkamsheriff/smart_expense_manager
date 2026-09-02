import { useMemo, useState } from 'react';
import { PageHeader } from '@/layouts/AppLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { CategoryBadge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { EmptyState } from '@/components/ui/EmptyState';
import { TableSkeleton, CardSkeleton } from '@/components/ui/Loading';
import { SelectInput } from '@/components/ui/FormField';
import { StatCard } from '@/components/ui/StatCard';
import { useAsync } from '@/hooks/useAsync';
import { incomeApi } from '@/api/income';
import { INCOME_CATEGORIES } from '@/constants/incomeCategories';
import { formatCurrency, formatDate } from '@/utils/format';
import { IncomeForm } from './IncomeForm';
import type { Income, NewIncome } from '@/types/income';

export function IncomePage() {
  const [category, setCategory] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Income | undefined>();
  const [deleting, setDeleting] = useState<Income | undefined>();
  const [deleteLoading, setDeleteLoading] = useState(false);

  const { data, loading, error, reload } = useAsync(() => incomeApi.list(category || undefined), [category]);
  const items = data ?? [];
  const total = items.reduce((s, i) => s + i.amount, 0);

  const openAdd = () => {
    setEditing(undefined);
    setModalOpen(true);
  };
  const openEdit = (income: Income) => {
    setEditing(income);
    setModalOpen(true);
  };

  const handleSubmit = async (data: NewIncome) => {
    if (editing) {
      await incomeApi.update(editing.id, data);
    } else {
      await incomeApi.create(data);
    }
    setModalOpen(false);
    reload();
  };

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteLoading(true);
    try {
      await incomeApi.remove(deleting.id);
      setDeleting(undefined);
      reload();
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div>
      <PageHeader title="Income" description="Track money coming in" actions={<Button onClick={openAdd}>Add Income</Button>} />

      <div className="mb-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
        {loading ? (
          <CardSkeleton />
        ) : (
          <StatCard label="Total Income" value={formatCurrency(total)} tone="emerald" />
        )}
      </div>

      <Card className="mb-4 p-4">
        <div className="max-w-xs">
          <SelectInput
            id="income-filter-category"
            label="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            options={[{ label: 'All categories', value: '' }, ...INCOME_CATEGORIES.map((c) => ({ label: c, value: c }))]}
          />
        </div>
      </Card>

      <Card>
        {loading ? (
          <TableSkeleton rows={5} cols={4} />
        ) : error ? (
          <p className="p-6 text-sm text-rose-500">Couldn't load income: {error}</p>
        ) : items.length === 0 ? (
          <EmptyState
            title="No income recorded yet"
            description="Add your first income entry to see it here."
            actionLabel="Add Income"
            onAction={openAdd}
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-faint">
                  <th className="px-5 py-3 font-medium">Source</th>
                  <th className="px-5 py-3 font-medium">Category</th>
                  <th className="px-5 py-3 font-medium">Date</th>
                  <th className="px-5 py-3 text-right font-medium">Amount</th>
                  <th className="px-5 py-3 text-right font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((i) => (
                  <tr key={i.id} className="border-b border-line last:border-0 hover:bg-paper/60">
                    <td className="px-5 py-3.5 font-medium">{i.source}</td>
                    <td className="px-5 py-3.5">
                      <CategoryBadge category={i.category} />
                    </td>
                    <td className="px-5 py-3.5 text-ink-soft">{formatDate(i.received_at)}</td>
                    <td className="num px-5 py-3.5 text-right font-semibold text-emerald-600">+{formatCurrency(i.amount)}</td>
                    <td className="px-5 py-3.5 text-right">
                      <div className="flex justify-end gap-1.5">
                        <Button size="sm" variant="ghost" onClick={() => openEdit(i)}>
                          Edit
                        </Button>
                        <Button size="sm" variant="ghost" className="text-rose-500 hover:bg-rose-50" onClick={() => setDeleting(i)}>
                          Delete
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Income' : 'Add Income'}>
        <IncomeForm initial={editing} onSubmit={handleSubmit} onCancel={() => setModalOpen(false)} />
      </Modal>

      <ConfirmDialog
        open={Boolean(deleting)}
        title="Delete income entry?"
        description={`This will permanently remove "${deleting?.source}". This can't be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleting(undefined)}
        loading={deleteLoading}
      />
    </div>
  );
}
