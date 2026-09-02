import { FormEvent, useState } from 'react';
import { Button } from '@/components/ui/Button';
import { TextInput, NumberInput, SelectInput } from '@/components/ui/FormField';
import { EXPENSE_CATEGORIES } from '@/constants/expenseCategories';
import type { RecurringExpense, NewRecurringExpense, Frequency } from '@/types/recurring';

interface RecurringFormProps {
  initial?: RecurringExpense;
  onSubmit: (data: NewRecurringExpense) => Promise<void>;
  onCancel: () => void;
}

const FREQUENCIES: { label: string; value: Frequency }[] = [
  { label: 'Daily', value: 'daily' },
  { label: 'Weekly', value: 'weekly' },
  { label: 'Monthly', value: 'monthly' },
  { label: 'Yearly', value: 'yearly' },
];

export function RecurringForm({ initial, onSubmit, onCancel }: RecurringFormProps) {
  const [description, setDescription] = useState(initial?.description ?? '');
  const [amount, setAmount] = useState(initial?.amount?.toString() ?? '');
  const [category, setCategory] = useState(initial?.category ?? EXPENSE_CATEGORIES[0]);
  const [frequency, setFrequency] = useState<Frequency>(initial?.frequency ?? 'monthly');
  const [startDate, setStartDate] = useState(initial?.start_date ?? new Date().toISOString().slice(0, 10));
  const [endDate, setEndDate] = useState(initial?.end_date ?? '');
  const [isActive, setIsActive] = useState(initial?.is_active ?? true);
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
      await onSubmit({
        description: description.trim(),
        amount: amountNum,
        category,
        frequency,
        start_date: startDate,
        end_date: endDate || null,
        is_active: isActive,
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <TextInput
        id="recurring-description"
        label="Description"
        placeholder="e.g. Netflix Subscription"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        error={errors.description}
        autoFocus
      />
      <div className="grid grid-cols-2 gap-4">
        <NumberInput
          id="recurring-amount"
          label="Amount"
          placeholder="0.00"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          error={errors.amount}
          min="0"
          step="0.01"
        />
        <SelectInput
          id="recurring-category"
          label="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          options={EXPENSE_CATEGORIES.map((c) => ({ label: c, value: c }))}
        />
      </div>
      <SelectInput
        id="recurring-frequency"
        label="Frequency"
        value={frequency}
        onChange={(e) => setFrequency(e.target.value as Frequency)}
        options={FREQUENCIES}
      />
      <div className="grid grid-cols-2 gap-4">
        <TextInput
          id="recurring-start"
          label="Start date"
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <TextInput
          id="recurring-end"
          label="End date (optional)"
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </div>
      <label className="flex items-center gap-2 text-sm font-medium text-ink">
        <input
          type="checkbox"
          checked={isActive}
          onChange={(e) => setIsActive(e.target.checked)}
          className="focus-ring h-4 w-4 rounded border-line text-emerald-500"
        />
        Active
      </label>
      <div className="mt-2 flex justify-end gap-2">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={submitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={submitting}>
          {submitting ? 'Saving…' : initial ? 'Save changes' : 'Add recurring expense'}
        </Button>
      </div>
    </form>
  );
}
