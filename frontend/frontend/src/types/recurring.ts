// NOT backed by Python yet. Forward-looking contract based on the product spec.

export type Frequency = 'daily' | 'weekly' | 'monthly' | 'yearly';

export interface RecurringExpense {
  id: number;
  description: string;
  amount: number;
  category: string;
  frequency: Frequency;
  start_date: string; // ISO date
  end_date?: string | null; // ISO date
  is_active: boolean;
  next_due_date: string; // ISO date, server-calculated
}

export type NewRecurringExpense = Omit<RecurringExpense, 'id' | 'next_due_date'>;
export type UpdateRecurringExpense = Partial<NewRecurringExpense>;
