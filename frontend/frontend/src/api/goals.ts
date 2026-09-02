import type {
  FinancialGoalWithProgress,
  NewFinancialGoal,
  UpdateFinancialGoal,
} from '@/types/goal';

import { apiClient } from './client';

type BackendGoal = {
  id: number;
  name: string;
  target_amount: number;
  current_amount: number;
  target_date: string;
  remaining: number;
  percentComplete: number;
};

function toGoal(item: BackendGoal): FinancialGoalWithProgress {
  return {
    id: item.id,
    name: item.name,
    target_amount: item.target_amount,
    current_amount: item.current_amount,
    target_date: item.target_date,
    remaining: item.remaining,
    percentComplete: item.percentComplete,
  };
}

export const goalsApi = {
  async list(): Promise<FinancialGoalWithProgress[]> {
    const items = await apiClient.get<BackendGoal[]>('/goals');

    return items.map(toGoal);
  },

  async create(
    data: NewFinancialGoal
  ): Promise<FinancialGoalWithProgress> {
    const created = await apiClient.post<BackendGoal>(
      '/goals',
      {
        name: data.name,
        target_amount: data.target_amount,
        current_amount: data.current_amount,
        target_date: data.target_date,
      }
    );

    return toGoal(created);
  },

  async update(
    id: number,
    data: UpdateFinancialGoal
  ): Promise<FinancialGoalWithProgress> {
    const updated = await apiClient.put<BackendGoal>(
      `/goals/${id}`,
      {
        name: data.name,
        target_amount: data.target_amount,
        current_amount: data.current_amount,
        target_date: data.target_date,
      }
    );

    return toGoal(updated);
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/goals/${id}`);
  },
};