// NOT backed by Python yet. Forward-looking contract based on the product spec.

export interface Budget {
  id: number;
  category: string;
  amount: number; // budgeted amount
  period: 'monthly' | 'yearly';
}

// Tracking data is a derived view: budget joined against actual spend for the period.
// Likely a computed endpoint (/api/budgets/{id}/tracking) rather than raw stored data.
export interface BudgetWithTracking extends Budget {
  spent: number;
  remaining: number;
  percentUsed: number;
}

export type NewBudget = Omit<Budget, 'id'>;
export type UpdateBudget = Partial<NewBudget>;
