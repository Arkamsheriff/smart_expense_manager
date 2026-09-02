import { FormEvent, useState } from 'react';
import { Button } from '@/components/ui/Button';
import { TextInput, NumberInput } from '@/components/ui/FormField';
import type { FinancialGoal, NewFinancialGoal } from '@/types/goal';

interface GoalFormProps {
  initial?: FinancialGoal;
  onSubmit: (data: NewFinancialGoal) => Promise<void>;
  onCancel: () => void;
}

export function GoalForm({ initial, onSubmit, onCancel }: GoalFormProps) {
  const [name, setName] = useState(initial?.name ?? '');
  const [targetAmount, setTargetAmount] = useState(initial?.target_amount?.toString() ?? '');
  const [currentAmount, setCurrentAmount] = useState(initial?.current_amount?.toString() ?? '0');
  const [targetDate, setTargetDate] = useState(initial?.target_date ?? '');
  const [errors, setErrors] = useState<{ name?: string; targetAmount?: string; targetDate?: string }>({});
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const nextErrors: typeof errors = {};
    if (!name.trim()) nextErrors.name = 'Goal name is required';
    const targetNum = parseFloat(targetAmount);
    if (!targetAmount || isNaN(targetNum) || targetNum <= 0) nextErrors.targetAmount = 'Enter an amount greater than 0';
    if (!targetDate) nextErrors.targetDate = 'Target date is required';
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    setSubmitting(true);
    try {
      await onSubmit({
        name: name.trim(),
        target_amount: targetNum,
        current_amount: parseFloat(currentAmount) || 0,
        target_date: targetDate,
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <TextInput
        id="goal-name"
        label="Goal name"
        placeholder="e.g. Emergency Fund"
        value={name}
        onChange={(e) => setName(e.target.value)}
        error={errors.name}
        autoFocus
      />
      <div className="grid grid-cols-2 gap-4">
        <NumberInput
          id="goal-target"
          label="Target amount"
          placeholder="0.00"
          value={targetAmount}
          onChange={(e) => setTargetAmount(e.target.value)}
          error={errors.targetAmount}
          min="0"
          step="0.01"
        />
        <NumberInput
          id="goal-current"
          label="Current amount"
          placeholder="0.00"
          value={currentAmount}
          onChange={(e) => setCurrentAmount(e.target.value)}
          min="0"
          step="0.01"
        />
      </div>
      <TextInput
        id="goal-date"
        label="Target date"
        type="date"
        value={targetDate}
        onChange={(e) => setTargetDate(e.target.value)}
        error={errors.targetDate}
      />
      <div className="mt-2 flex justify-end gap-2">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={submitting}>
          Cancel
        </Button>
        <Button type="submit" disabled={submitting}>
          {submitting ? 'Saving…' : initial ? 'Save changes' : 'Create goal'}
        </Button>
      </div>
    </form>
  );
}
