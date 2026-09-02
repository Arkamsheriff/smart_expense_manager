// Backed by a real Python module today: app/reports/report_service.py + visualization.py + csv_exporter.py

import type { Expense } from './expense';

export interface SpendingStatistics {
  count: number;
  total: number;
  average: number;
  highest: number;
  lowest: number;
}

export interface CategorySummaryItem {
  category: string;
  total: number;
  count: number;
  percentOfTotal: number;
}

export interface PeriodReport {
  expenses: Expense[];
  total: number;
}
