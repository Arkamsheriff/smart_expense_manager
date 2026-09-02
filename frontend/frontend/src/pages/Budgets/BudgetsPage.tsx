import { useState } from 'react';
import { PageHeader } from '@/layouts/AppLayout';
import { Card, CardBody } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { EmptyState } from '@/components/ui/EmptyState';
import { CardSkeleton } from '@/components/ui/Loading';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { useAsync } from '@/hooks/useAsync';
import { budgetsApi } from '@/api/budgets';
import { formatCurrency, formatPercent } from '@/utils/format';
import { BudgetForm } from './BudgetForm';
import type { Budget, BudgetWithTracking, NewBudget } from '@/types/budget';

export function BudgetsPage() {
  const { data, loading, error, reload } = useAsync(() => budgetsApi.list());
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<BudgetWithTracking | undefined>();
  const [deleting, setDeleting] = useState<BudgetWithTracking | undefined>();
  const [deleteLoading, setDeleteLoading] = useState(false);

  const items = data ?? [];

  const openAdd = () => {
    setEditing(undefined);
    setModalOpen(true);
  };
  const openEdit = (b: BudgetWithTracking) => {
    setEditing(b);
    setModalOpen(true);
  };

  const handleSubmit = async (data: NewBudget) => {
    if (editing) {
      await budgetsApi.update(editing.id, data);
    } else {
      await budgetsApi.create(data);
    }
    setModalOpen(false);
    reload();
  };

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteLoading(true);
    try {
      await budgetsApi.remove(deleting.id);
      setDeleting(undefined);
      reload();
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div>
      <PageHeader
        title="Budgets"
        description="Set spending limits by category"
        actions={<Button onClick={openAdd}>Create Budget</Button>}
      />

      {loading ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      ) : error ? (
        <p className="text-sm text-rose-500">Couldn't load budgets: {error}</p>
      ) : items.length === 0 ? (
        <Card>
          <EmptyState
            title="No budgets yet"
            description="Set a spending limit for a category to start tracking against it."
            actionLabel="Create Budget"
            onAction={openAdd}
          />
        </Card>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {items.map((b) => {
            const over = b.percentUsed >= 100;
            return (
              <Card key={b.id}>
                <CardBody>
                  <div className="mb-3 flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold">{b.category}</h3>
                      <span className="text-xs capitalize text-ink-faint">{b.period}</span>
                    </div>
                    <div className="flex gap-1">
                      <Button size="sm" variant="ghost" onClick={() => openEdit(b)}>
                        Edit
                      </Button>
                      <Button size="sm" variant="ghost" className="text-rose-500 hover:bg-rose-50" onClick={() => setDeleting(b)}>
                        Delete
                      </Button>
                    </div>
                  </div>

                  <div className="mb-2 flex items-baseline justify-between">
                    <span className="num text-lg font-semibold">{formatCurrency(b.spent)}</span>
                    <span className="num text-sm text-ink-soft">of {formatCurrency(b.amount)}</span>
                  </div>
                  <ProgressBar percent={b.percentUsed} />
                  <div className="mt-2 flex items-center justify-between text-xs">
                    <span className={over ? 'font-medium text-rose-500' : 'text-ink-soft'}>
                      {over ? 'Over budget' : `${formatCurrency(b.remaining)} remaining`}
                    </span>
                    <span className="num text-ink-faint">{formatPercent(b.percentUsed)}</span>
                  </div>
                </CardBody>
              </Card>
            );
          })}
        </div>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Budget' : 'Create Budget'}>
        <BudgetForm initial={editing} onSubmit={handleSubmit} onCancel={() => setModalOpen(false)} />
      </Modal>

      <ConfirmDialog
        open={Boolean(deleting)}
        title="Delete budget?"
        description={`This will remove the ${deleting?.category} budget. This can't be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleting(undefined)}
        loading={deleteLoading}
      />
    </div>
  );
}
