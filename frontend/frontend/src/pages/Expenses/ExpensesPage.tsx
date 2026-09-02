import { useMemo, useState } from 'react';
import { PageHeader } from '@/layouts/AppLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { CategoryBadge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { EmptyState } from '@/components/ui/EmptyState';
import { TableSkeleton } from '@/components/ui/Loading';
import { TextInput, SelectInput, NumberInput } from '@/components/ui/FormField';
import { useAsync } from '@/hooks/useAsync';
import { expensesApi } from '@/api/expenses';
import { EXPENSE_CATEGORIES } from '@/constants/expenseCategories';
import { formatCurrency, formatDateTime } from '@/utils/format';
import { ExpenseForm } from './ExpenseForm';
import type { Expense, NewExpense } from '@/types/expense';

const PAGE_SIZE = 8;

export function ExpensesPage() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [minAmount, setMinAmount] = useState('');
  const [maxAmount, setMaxAmount] = useState('');
  const [page, setPage] = useState(1);

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Expense | undefined>();
  const [deleting, setDeleting] = useState<Expense | undefined>();
  const [deleteLoading, setDeleteLoading] = useState(false);

  const filters = useMemo(
    () => ({
      search: search || undefined,
      category: category || undefined,
      minAmount: minAmount ? parseFloat(minAmount) : undefined,
      maxAmount: maxAmount ? parseFloat(maxAmount) : undefined,
    }),
    [search, category, minAmount, maxAmount]
  );

  const { data, loading, error, reload } = useAsync(() => expensesApi.list(filters), [
    filters.search,
    filters.category,
    filters.minAmount,
    filters.maxAmount,
  ]);

  const items = data ?? [];
  const totalPages = Math.max(1, Math.ceil(items.length / PAGE_SIZE));
  const pageItems = items.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  const openAdd = () => {
    setEditing(undefined);
    setModalOpen(true);
  };
  const openEdit = (expense: Expense) => {
    setEditing(expense);
    setModalOpen(true);
  };

  const handleSubmit = async (data: NewExpense) => {
    if (editing) {
      await expensesApi.update(editing.id, data);
    } else {
      await expensesApi.create(data);
    }
    setModalOpen(false);
    setPage(1);
    reload();
  };

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteLoading(true);
    try {
      await expensesApi.remove(deleting.id);
      setDeleting(undefined);
      reload();
    } finally {
      setDeleteLoading(false);
    }
  };

  const hasFilters = Boolean(search || category || minAmount || maxAmount);

  return (
    <div>
      <PageHeader
        title="Expenses"
        description="Track and manage every expense"
        actions={<Button onClick={openAdd}>Add Expense</Button>}
      />

      <Card className="mb-4 p-4">
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <TextInput
            id="search"
            label="Search"
            placeholder="Search description…"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
          <SelectInput
            id="filter-category"
            label="Category"
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              setPage(1);
            }}
            options={[{ label: 'All categories', value: '' }, ...EXPENSE_CATEGORIES.map((c) => ({ label: c, value: c }))]}
          />
          <NumberInput
            id="min-amount"
            label="Min amount"
            placeholder="0"
            value={minAmount}
            onChange={(e) => {
              setMinAmount(e.target.value);
              setPage(1);
            }}
          />
          <NumberInput
            id="max-amount"
            label="Max amount"
            placeholder="No limit"
            value={maxAmount}
            onChange={(e) => {
              setMaxAmount(e.target.value);
              setPage(1);
            }}
          />
        </div>
      </Card>

      <Card>
        {loading ? (
          <TableSkeleton rows={6} cols={4} />
        ) : error ? (
          <p className="p-6 text-sm text-rose-500">Couldn't load expenses: {error}</p>
        ) : items.length === 0 ? (
          <EmptyState
            title={hasFilters ? 'No expenses match your filters' : 'No expenses yet'}
            description={
              hasFilters
                ? 'Try adjusting your search or filters.'
                : 'Add your first expense to start tracking your spending.'
            }
            actionLabel={hasFilters ? undefined : 'Add Expense'}
            onAction={hasFilters ? undefined : openAdd}
          />
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
                    <th className="px-5 py-3 text-right font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {pageItems.map((e) => (
                    <tr key={e.id} className="border-b border-line last:border-0 hover:bg-paper/60">
                      <td className="px-5 py-3.5 font-medium">{e.description}</td>
                      <td className="px-5 py-3.5">
                        <CategoryBadge category={e.category} />
                      </td>
                      <td className="px-5 py-3.5 text-ink-soft">{formatDateTime(e.created_at)}</td>
                      <td className="num px-5 py-3.5 text-right font-semibold text-rose-500">
                        -{formatCurrency(e.amount)}
                      </td>
                      <td className="px-5 py-3.5 text-right">
                        <div className="flex justify-end gap-1.5">
                          <Button size="sm" variant="ghost" onClick={() => openEdit(e)}>
                            Edit
                          </Button>
                          <Button size="sm" variant="ghost" className="text-rose-500 hover:bg-rose-50" onClick={() => setDeleting(e)}>
                            Delete
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {totalPages > 1 && (
              <div className="flex items-center justify-between border-t border-line px-5 py-3 text-sm">
                <span className="text-ink-soft">
                  Page {page} of {totalPages} · {items.length} expenses
                </span>
                <div className="flex gap-2">
                  <Button size="sm" variant="secondary" disabled={page === 1} onClick={() => setPage((p) => p - 1)}>
                    Previous
                  </Button>
                  <Button size="sm" variant="secondary" disabled={page === totalPages} onClick={() => setPage((p) => p + 1)}>
                    Next
                  </Button>
                </div>
              </div>
            )}
          </>
        )}
      </Card>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Expense' : 'Add Expense'}>
        <ExpenseForm initial={editing} onSubmit={handleSubmit} onCancel={() => setModalOpen(false)} />
      </Modal>

      <ConfirmDialog
        open={Boolean(deleting)}
        title="Delete expense?"
        description={`This will permanently remove "${deleting?.description}". This can't be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleting(undefined)}
        loading={deleteLoading}
      />
    </div>
  );
}
