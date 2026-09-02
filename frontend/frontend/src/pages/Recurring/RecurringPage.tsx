import { useState } from 'react';
import { PageHeader } from '@/layouts/AppLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { CategoryBadge, StatusBadge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { EmptyState } from '@/components/ui/EmptyState';
import { TableSkeleton } from '@/components/ui/Loading';
import { useAsync } from '@/hooks/useAsync';
import { recurringApi } from '@/api/recurring';
import { formatCurrency, formatDate } from '@/utils/format';
import { RecurringForm } from './RecurringForm';
import type { RecurringExpense, NewRecurringExpense } from '@/types/recurring';

const FREQUENCY_LABEL: Record<string, string> = {
  daily: 'Daily',
  weekly: 'Weekly',
  monthly: 'Monthly',
  yearly: 'Yearly',
};

export function RecurringPage() {
  const { data, loading, error, reload } = useAsync(() => recurringApi.list());
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<RecurringExpense | undefined>();
  const [deleting, setDeleting] = useState<RecurringExpense | undefined>();
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [togglingId, setTogglingId] = useState<number | null>(null);

  const items = data ?? [];

  const openAdd = () => {
    setEditing(undefined);
    setModalOpen(true);
  };
  const openEdit = (item: RecurringExpense) => {
    setEditing(item);
    setModalOpen(true);
  };

  const handleSubmit = async (data: NewRecurringExpense) => {
    if (editing) {
      await recurringApi.update(editing.id, data);
    } else {
      await recurringApi.create(data);
    }
    setModalOpen(false);
    reload();
  };

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteLoading(true);
    try {
      await recurringApi.remove(deleting.id);
      setDeleting(undefined);
      reload();
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleToggle = async (item: RecurringExpense) => {
    setTogglingId(item.id);
    try {
      await recurringApi.toggleActive(item.id);
      reload();
    } finally {
      setTogglingId(null);
    }
  };

  return (
    <div>
      <PageHeader
        title="Recurring Expenses"
        description="Manage subscriptions and repeating charges"
        actions={<Button onClick={openAdd}>Add Recurring Expense</Button>}
      />

      <Card>
        {loading ? (
          <TableSkeleton rows={5} cols={6} />
        ) : error ? (
          <p className="p-6 text-sm text-rose-500">Couldn't load recurring expenses: {error}</p>
        ) : items.length === 0 ? (
          <EmptyState
            title="No recurring expenses yet"
            description="Add subscriptions or bills that repeat on a schedule."
            actionLabel="Add Recurring Expense"
            onAction={openAdd}
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-faint">
                  <th className="px-5 py-3 font-medium">Description</th>
                  <th className="px-5 py-3 font-medium">Category</th>
                  <th className="px-5 py-3 font-medium">Frequency</th>
                  <th className="px-5 py-3 font-medium">Next Due</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 text-right font-medium">Amount</th>
                  <th className="px-5 py-3 text-right font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((r) => (
                  <tr key={r.id} className="border-b border-line last:border-0 hover:bg-paper/60">
                    <td className="px-5 py-3.5 font-medium">{r.description}</td>
                    <td className="px-5 py-3.5">
                      <CategoryBadge category={r.category} />
                    </td>
                    <td className="px-5 py-3.5 text-ink-soft">{FREQUENCY_LABEL[r.frequency]}</td>
                    <td className="px-5 py-3.5 text-ink-soft">{formatDate(r.next_due_date)}</td>
                    <td className="px-5 py-3.5">
                      <StatusBadge active={r.is_active} />
                    </td>
                    <td className="num px-5 py-3.5 text-right font-semibold">{formatCurrency(r.amount)}</td>
                    <td className="px-5 py-3.5 text-right">
                      <div className="flex justify-end gap-1.5">
                        <Button size="sm" variant="ghost" disabled={togglingId === r.id} onClick={() => handleToggle(r)}>
                          {togglingId === r.id ? '…' : r.is_active ? 'Deactivate' : 'Activate'}
                        </Button>
                        <Button size="sm" variant="ghost" onClick={() => openEdit(r)}>
                          Edit
                        </Button>
                        <Button size="sm" variant="ghost" className="text-rose-500 hover:bg-rose-50" onClick={() => setDeleting(r)}>
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

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? 'Edit Recurring Expense' : 'Add Recurring Expense'}
      >
        <RecurringForm initial={editing} onSubmit={handleSubmit} onCancel={() => setModalOpen(false)} />
      </Modal>

      <ConfirmDialog
        open={Boolean(deleting)}
        title="Delete recurring expense?"
        description={`This will stop and remove "${deleting?.description}". This can't be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleting(undefined)}
        loading={deleteLoading}
      />
    </div>
  );
}
