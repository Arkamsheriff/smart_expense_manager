import { FormEvent, useState } from 'react';
import { Button } from '@/components/ui/Button';
import { TextInput, NumberInput, SelectInput } from '@/components/ui/FormField';
import { INCOME_CATEGORIES } from '@/constants/incomeCategories';
import type { Income, NewIncome } from '@/types/income';

interface IncomeFormProps {
  initial?: Income;
  onSubmit: (data: NewIncome) => Promise<void>;
  onCancel: () => void;
}

export function IncomeForm({ initial, onSubmit, onCancel }: IncomeFormProps) {
  const [source, setSource] = useState(initial?.source ?? '');
  const [amount, setAmount] = useState(initial?.amount?.toString() ?? '');
  const [category, setCategory] = useState(initial?.category ?? INCOME_CATEGORIES[0]);
  const [receivedAt, setReceivedAt] = useState(initial?.received_at?.slice(0, 10) ?? new Date().toISOString().slice(0, 10));
  const [errors, setErrors] = useState<{ source?: string; amount?: string }>({});
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const nextErrors: typeof errors = {};
    if (!source.trim()) nextErrors.source = 'Source is required';
    const amountNum = parseFloat(amount);
    if (!amount || isNaN(amountNum) || amountNum <= 0) nextErrors.amount = 'Enter an amount greater than 0';
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    setSubmitting(true);
    try {
      await onSubmit({
        source: source.trim(),
        amount: amountNum,
        category,
        received_at: new Date(receivedAt).toISOString(),
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <TextInput
        id="income-source"
        label="Source"
        placeholder="e.g. Salary - Acme Corp"
        value={source}
        onChange={(e) => setSource(e.target.value)}
        error={errors.source}
        autoFocus
      />
      <NumberInput
        id="income-amount"
        label="Amount"
        placeholder="0.00"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        error={errors.amount}
        min="0"
        step="0.01"
      />
      <SelectInput
        id="income-category"
        label="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        options={INCOME_CATEGORIES.map((c) => ({ label: c, value: c }))}
      />
      <TextInput
        id="income-date"
        label="Date received"
        type="date"
        value={receivedAt}
        onChange={(e) => setReceivedAt(e.target.value)}
      />
      <div className="mt-2 flex justify-end gap-2">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={submitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={submitting}>
          {submitting ? 'Saving…' : initial ? 'Save changes' : 'Add income'}
        </Button>
      </div>
    </form>
  );
}
