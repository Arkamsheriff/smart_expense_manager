// Backed by a real Python module today: app/expense_manager.py + app/database/repository.py
// Field names mirror the CSV export sample in the repo README (ID, Description, Amount, Category, Created At).
// Confirm exact field names/types against expense.py before wiring up FastAPI.

export interface Expense {
  id: number;
  description: string;
  amount: number;
  category: string;
  created_at: string; // ISO datetime string
}

export type NewExpense = Omit<Expense, 'id' | 'created_at'>;
export type UpdateExpense = Partial<NewExpense>;

export interface ExpenseFilters {
  search?: string;
  category?: string;
  minAmount?: number;
  maxAmount?: number;
}

export interface ExpenseCategoryTotal {
  category: string;
  total: number;
}
