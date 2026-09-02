import type {
  Budget,
  NewBudget,
  BudgetWithTracking,
} from '@/types/budget';

import { apiClient } from './client';

type BackendBudget = {
  id: number;
  category: string;
  amount: number;
  period: 'monthly' | 'yearly';
  spent: number;
  remaining: number;
  percentUsed: number;
};

function toBudget(item: BackendBudget): BudgetWithTracking {
  return {
    id: item.id,
    category: item.category,
    amount: item.amount,
    period: item.period,
    spent: item.spent,
    remaining: item.remaining,
    percentUsed: item.percentUsed,
  };
}

export const budgetsApi = {
  async list(): Promise<BudgetWithTracking[]> {
    const items = await apiClient.get<BackendBudget[]>('/budgets');

    return items.map(toBudget);
  },

  async create(data: NewBudget): Promise<Budget> {
    const created = await apiClient.post<BackendBudget>(
      '/budgets',
      {
        category: data.category,
        amount: data.amount,
        period: data.period,
      }
    );

    return toBudget(created);
  },

  async update(
    id: number,
    data: Partial<NewBudget>
  ): Promise<Budget> {
    const updated = await apiClient.put<BackendBudget>(
      `/budgets/${id}`,
      {
        category: data.category,
        amount: data.amount,
        period: data.period,
      }
    );

    return toBudget(updated);
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/budgets/${id}`);
  },
};