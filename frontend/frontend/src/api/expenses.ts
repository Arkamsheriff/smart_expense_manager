import type {
  Expense,
  NewExpense,
  UpdateExpense,
} from '@/types/expense';

import { apiClient } from './client';

type BackendExpense = {
  id: number;
  description: string;
  amount: number;
  category: string;
  created_at: string;
};

type ExpenseFilters = {
  search?: string;
  category?: string;
};

function toExpense(item: BackendExpense): Expense {
  return {
    id: item.id,
    description: item.description,
    amount: item.amount,
    category: item.category,
    created_at: item.created_at,
  };
}

export const expensesApi = {
  async list(filters?: ExpenseFilters): Promise<Expense[]> {
    const items = await apiClient.get<BackendExpense[]>('/expenses');

    let expenses = items.map(toExpense);

    if (filters?.category && filters.category !== 'All') {
      expenses = expenses.filter(
        (expense) =>
          expense.category.toLowerCase() ===
          filters.category!.toLowerCase()
      );
    }

    if (filters?.search) {
      const search = filters.search.toLowerCase();

      expenses = expenses.filter((expense) =>
        expense.description.toLowerCase().includes(search)
      );
    }

    return expenses;
  },

  async create(data: NewExpense): Promise<Expense> {
    const created = await apiClient.post<BackendExpense>(
      '/expenses',
      {
        description: data.description,
        amount: data.amount,
        category: data.category,
      }
    );

    return toExpense(created);
  },

  async update(
    id: number,
    data: UpdateExpense
  ): Promise<Expense> {
    const updated = await apiClient.put<BackendExpense>(
      `/expenses/${id}`,
      {
        description: data.description,
        amount: data.amount,
        category: data.category,
      }
    );

    return toExpense(updated);
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/expenses/${id}`);
  },
};