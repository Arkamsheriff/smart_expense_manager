import { FormEvent, useState } from 'react';
import { Button } from '@/components/ui/Button';
import { TextInput, NumberInput, SelectInput } from '@/components/ui/FormField';
import { EXPENSE_CATEGORIES } from '@/constants/expenseCategories';
import type { Expense, NewExpense } from '@/types/expense';

interface ExpenseFormProps {
  initial?: Expense;
  onSubmit: (data: NewExpense) => Promise<void>;
  onCancel: () => void;
}

export function ExpenseForm({ initial, onSubmit, onCancel }: ExpenseFormProps) {
  const [description, setDescription] = useState(initial?.description ?? '');
  const [amount, setAmount] = useState(initial?.amount?.toString() ?? '');
  const [category, setCategory] = useState(initial?.category ?? EXPENSE_CATEGORIES[0]);
  const [errors, setErrors] = useState<{ description?: string; amount?: string }>({});
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const nextErrors: typeof errors = {};
    if (!description.trim()) nextErrors.description = 'Description is required';
    const amountNum = parseFloat(amount);
    if (!amount || isNaN(amountNum) || amountNum <= 0) nextErrors.amount = 'Enter an amount greater than 0';
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    setSubmitting(true);
    try {
      await onSubmit({ description: description.trim(), amount: amountNum, category });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <TextInput
        id="expense-description"
        label="Description"
        placeholder="e.g. Groceries"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        error={errors.description}
        autoFocus
      />
      <NumberInput
        id="expense-amount"
        label="Amount"
        placeholder="0.00"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        error={errors.amount}
        min="0"
        step="0.01"
      />
      <SelectInput
        id="expense-category"
        label="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        options={EXPENSE_CATEGORIES.map((c) => ({ label: c, value: c }))}
      />
      <div className="mt-2 flex justify-end gap-2">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={submitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={submitting}>
          {submitting ? 'Saving…' : initial ? 'Save changes' : 'Add expense'}
        </Button>
      </div>
    </form>
  );
}
