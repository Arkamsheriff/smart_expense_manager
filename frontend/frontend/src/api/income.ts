import type { Income, NewIncome, UpdateIncome } from '@/types/income';
import { apiClient } from './client';

type BackendIncome = {
  id: number;
  description: string;
  amount: number;
  category: string;
  created_at: string;
};

function toIncome(item: BackendIncome): Income {
  return {
    id: item.id,
    source: item.description,
    amount: item.amount,
    category: item.category,
    received_at: item.created_at,
  };
}

function toBackendPayload(
  data: NewIncome | UpdateIncome
): {
  description: string;
  amount: number;
  category: string;
} {
  if (
    data.source === undefined ||
    data.amount === undefined ||
    data.category === undefined
  ) {
    throw new Error('Source, amount, and category are required');
  }

  return {
    description: data.source,
    amount: data.amount,
    category: data.category,
  };
}

export const incomeApi = {
  async list(category?: string): Promise<Income[]> {
    const items = await apiClient.get<BackendIncome[]>('/income');

    const incomes = items.map(toIncome);

    if (category) {
      return incomes.filter(
        (item) =>
          item.category.toLowerCase() === category.toLowerCase()
      );
    }

    return incomes;
  },

  async create(data: NewIncome): Promise<Income> {
    const created = await apiClient.post<BackendIncome>(
      '/income',
      toBackendPayload(data)
    );

    return toIncome(created);
  },

  async update(id: number, data: UpdateIncome): Promise<Income> {
    const updated = await apiClient.put<BackendIncome>(
      `/income/${id}`,
      toBackendPayload(data)
    );

    return toIncome(updated);
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/income/${id}`);
  },
};