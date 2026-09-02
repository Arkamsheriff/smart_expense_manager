import type {
  SpendingStatistics,
  CategorySummaryItem,
  PeriodReport,
} from '@/types/report';

import type { DashboardSummary } from '@/types/dashboard';

import { apiClient } from './client';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api';

export const reportsApi = {
  today: (): Promise<PeriodReport> =>
    apiClient.get<PeriodReport>('/reports/today'),

  weekly: (): Promise<PeriodReport> =>
    apiClient.get<PeriodReport>('/reports/weekly'),

  monthly: (): Promise<PeriodReport> =>
    apiClient.get<PeriodReport>('/reports/monthly'),

  categorySummary: (): Promise<CategorySummaryItem[]> =>
    apiClient.get<CategorySummaryItem[]>('/reports/category-summary'),

  statistics: (): Promise<SpendingStatistics> =>
    apiClient.get<SpendingStatistics>('/reports/statistics'),

  monthlySeries: (): Promise<{ month: string; total: number }[]> =>
    apiClient.get<{ month: string; total: number }[]>(
      '/reports/monthly-series'
    ),

  exportCsv: async (): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/reports/export-csv`);

    if (!response.ok) {
      const message = await response.text().catch(() => '');
      throw new Error(message || 'Failed to export CSV');
    }

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = 'expenses.csv';

    document.body.appendChild(link);
    link.click();
    link.remove();

    window.URL.revokeObjectURL(url);
  },
};

export const dashboardApi = {
  summary: (): Promise<DashboardSummary> =>
    apiClient.get<DashboardSummary>('/dashboard/summary'),
};