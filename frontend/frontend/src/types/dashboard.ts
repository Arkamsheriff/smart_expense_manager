// Aggregated data returned by the FastAPI dashboard summary endpoint.

import type { Expense } from './expense';
import type { Income } from './income';
import type { RecurringExpense } from './recurring';
import type { FinancialGoalWithProgress } from './goal';
import type { BudgetWithTracking } from './budget';

export interface DashboardSummary {
  totalIncome: number;
  totalExpenses: number;
  currentBalance: number;
  savingsRate: number; // percentage
  recentExpenses: Expense[];
  recentIncome: Income[];
  upcomingRecurring: RecurringExpense[];
  goals: FinancialGoalWithProgress[];
  budgets: BudgetWithTracking[];
  expenseByCategory: { category: string; total: number }[];
  incomeVsExpenseByMonth: {
    month: string;
    income: number;
    expenses: number;
  }[];
}