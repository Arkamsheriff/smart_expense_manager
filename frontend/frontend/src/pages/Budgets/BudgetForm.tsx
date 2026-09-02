import { FormEvent, useState } from 'react';
import { Button } from '@/components/ui/Button';
import { NumberInput, SelectInput } from '@/components/ui/FormField';
import { EXPENSE_CATEGORIES } from '@/constants/expenseCategories';
import type { Budget, NewBudget } from '@/types/budget';

interface BudgetFormProps {
  initial?: Budget;
  onSubmit: (data: NewBudget) => Promise<void>;
  onCancel: () => void;
}

export function BudgetForm({ initial, onSubmit, onCancel }: BudgetFormProps) {
  const [category, setCategory] = useState(initial?.category ?? EXPENSE_CATEGORIES[0]);
  const [amount, setAmount] = useState(initial?.amount?.toString() ?? '');
  const [period, setPeriod] = useState<'monthly' | 'yearly'>(initial?.period ?? 'monthly');
  const [error, setError] = useState<string | undefined>();
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const amountNum = parseFloat(amount);
    if (!amount || isNaN(amountNum) || amountNum <= 0) {
      setError('Enter an amount greater than 0');
      return;
    }
    setError(undefined);
    setSubmitting(true);
    try {
      await onSubmit({ category, amount: amountNum, period });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <SelectInput
        id="budget-category"
        label="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        options={EXPENSE_CATEGORIES.map((c) => ({ label: c, value: c }))}
      />
      <NumberInput
        id="budget-amount"
        label="Budget amount"
        placeholder="0.00"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        error={error}
        min="0"
        step="0.01"
        autoFocus
      />
      <SelectInput
        id="budget-period"
        label="Period"
        value={period}
        onChange={(e) => setPeriod(e.target.value as 'monthly' | 'yearly')}
        options={[
          { label: 'Monthly', value: 'monthly' },
          { label: 'Yearly', value: 'yearly' },
        ]}
      />
      <div className="mt-2 flex justify-end gap-2">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={submitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={submitting}>
          {submitting ? 'Saving…' : initial ? 'Save changes' : 'Create budget'}
        </Button>
      </div>
    </form>
  );
}
