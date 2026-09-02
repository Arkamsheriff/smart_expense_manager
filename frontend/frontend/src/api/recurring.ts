import type {
  RecurringExpense,
  NewRecurringExpense,
  UpdateRecurringExpense,
} from '@/types/recurring';

import { apiClient } from './client';

type BackendFrequency = 'Daily' | 'Weekly' | 'Monthly' | 'Yearly';

type BackendRecurringExpense = {
  id: number;
  description: string;
  amount: number;
  category: string;
  frequency: BackendFrequency;
  start_date: string;
  end_date: string | null;
  active: boolean;
};

type NextDueResponse = string | null;

function toFrontendFrequency(
  frequency: BackendFrequency
): RecurringExpense['frequency'] {
  return frequency.toLowerCase() as RecurringExpense['frequency'];
}

function toBackendFrequency(
  frequency: RecurringExpense['frequency']
): BackendFrequency {
  const frequencyMap: Record<
    RecurringExpense['frequency'],
    BackendFrequency
  > = {
    daily: 'Daily',
    weekly: 'Weekly',
    monthly: 'Monthly',
    yearly: 'Yearly',
  };

  return frequencyMap[frequency];
}

function toRecurringExpense(
  item: BackendRecurringExpense,
  nextDueDate: string | null
): RecurringExpense {
  return {
    id: item.id,
    description: item.description,
    amount: item.amount,
    category: item.category,
    frequency: toFrontendFrequency(item.frequency),
    start_date: item.start_date,
    end_date: item.end_date,
    is_active: item.active,
    next_due_date: nextDueDate ?? '',
  };
}

function toBackendPayload(data: {
  description: string;
  amount: number;
  category: string;
  frequency: RecurringExpense['frequency'];
  start_date: string;
  end_date?: string | null;
  is_active: boolean;
}) {
  return {
    description: data.description,
    amount: data.amount,
    category: data.category,
    frequency: toBackendFrequency(data.frequency),
    start_date: data.start_date,
    end_date: data.end_date ?? null,
    active: data.is_active,
  };
}

async function getNextDueDate(id: number): Promise<string | null> {
  return apiClient.get<NextDueResponse>(
    `/recurring/${id}/next-due`
  );
}

async function mapRecurringExpense(
  item: BackendRecurringExpense
): Promise<RecurringExpense> {
  const nextDueDate = await getNextDueDate(item.id);

  return toRecurringExpense(item, nextDueDate);
}

export const recurringApi = {
  async list(): Promise<RecurringExpense[]> {
    const items = await apiClient.get<BackendRecurringExpense[]>(
      '/recurring'
    );

    return Promise.all(items.map(mapRecurringExpense));
  },

  async create(data: NewRecurringExpense): Promise<RecurringExpense> {
    const created = await apiClient.post<BackendRecurringExpense>(
      '/recurring',
      toBackendPayload(data)
    );

    return mapRecurringExpense(created);
  },

  async update(
    id: number,
    data: UpdateRecurringExpense
  ): Promise<RecurringExpense> {
    const existing = await apiClient.get<BackendRecurringExpense>(
      `/recurring/${id}`
    );

    const merged: NewRecurringExpense = {
      description: data.description ?? existing.description,
      amount: data.amount ?? existing.amount,
      category: data.category ?? existing.category,
      frequency:
        data.frequency ??
        toFrontendFrequency(existing.frequency),
      start_date: data.start_date ?? existing.start_date,
      end_date: data.end_date ?? existing.end_date,
      is_active: data.is_active ?? existing.active,
    };

    const updated = await apiClient.put<BackendRecurringExpense>(
      `/recurring/${id}`,
      toBackendPayload(merged)
    );

    return mapRecurringExpense(updated);
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/recurring/${id}`);
  },

  async toggleActive(id: number): Promise<RecurringExpense> {
    const updated = await apiClient.patch<BackendRecurringExpense>(
      `/recurring/${id}/toggle`,
      {}
    );

    return mapRecurringExpense(updated);
  },
};