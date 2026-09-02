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
import { goalsApi } from '@/api/goals';
import { formatCurrency, formatDate, formatPercent } from '@/utils/format';
import { GoalForm } from './GoalForm';
import type { FinancialGoalWithProgress, NewFinancialGoal } from '@/types/goal';

export function GoalsPage() {
  const { data, loading, error, reload } = useAsync(() => goalsApi.list());
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<FinancialGoalWithProgress | undefined>();
  const [deleting, setDeleting] = useState<FinancialGoalWithProgress | undefined>();
  const [deleteLoading, setDeleteLoading] = useState(false);

  const items = data ?? [];

  const openAdd = () => {
    setEditing(undefined);
    setModalOpen(true);
  };
  const openEdit = (g: FinancialGoalWithProgress) => {
    setEditing(g);
    setModalOpen(true);
  };

  const handleSubmit = async (data: NewFinancialGoal) => {
    if (editing) {
      await goalsApi.update(editing.id, data);
    } else {
      await goalsApi.create(data);
    }
    setModalOpen(false);
    reload();
  };

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteLoading(true);
    try {
      await goalsApi.remove(deleting.id);
      setDeleting(undefined);
      reload();
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div>
      <PageHeader
        title="Financial Goals"
        description="Save toward what matters"
        actions={<Button onClick={openAdd}>Create Goal</Button>}
      />

      {loading ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      ) : error ? (
        <p className="text-sm text-rose-500">Couldn't load goals: {error}</p>
      ) : items.length === 0 ? (
        <Card>
          <EmptyState
            title="No goals yet"
            description="Create a savings goal to track your progress toward it."
            actionLabel="Create Goal"
            onAction={openAdd}
          />
        </Card>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {items.map((g) => {
            const complete = g.percentComplete >= 100;
            return (
              <Card key={g.id}>
                <CardBody>
                  <div className="mb-3 flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold">{g.name}</h3>
                      <span className="text-xs text-ink-faint">Target {formatDate(g.target_date)}</span>
                    </div>
                    <div className="flex gap-1">
                      <Button size="sm" variant="ghost" onClick={() => openEdit(g)}>
                        Edit
                      </Button>
                      <Button size="sm" variant="ghost" className="text-rose-500 hover:bg-rose-50" onClick={() => setDeleting(g)}>
                        Delete
                      </Button>
                    </div>
                  </div>

                  <div className="mb-2 flex items-baseline justify-between">
                    <span className="num text-lg font-semibold">{formatCurrency(g.current_amount)}</span>
                    <span className="num text-sm text-ink-soft">of {formatCurrency(g.target_amount)}</span>
                  </div>
                  <ProgressBar percent={g.percentComplete} tone={complete ? 'emerald' : undefined} />
                  <div className="mt-2 flex items-center justify-between text-xs">
                    <span className={complete ? 'font-medium text-emerald-600' : 'text-ink-soft'}>
                      {complete ? 'Goal reached' : `${formatCurrency(g.remaining)} to go`}
                    </span>
                    <span className="num text-ink-faint">{formatPercent(g.percentComplete)}</span>
                  </div>
                </CardBody>
              </Card>
            );
          })}
        </div>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Goal' : 'Create Goal'}>
        <GoalForm initial={editing} onSubmit={handleSubmit} onCancel={() => setModalOpen(false)} />
      </Modal>

      <ConfirmDialog
        open={Boolean(deleting)}
        title="Delete goal?"
        description={`This will remove "${deleting?.name}". This can't be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleting(undefined)}
        loading={deleteLoading}
      />
    </div>
  );
}
