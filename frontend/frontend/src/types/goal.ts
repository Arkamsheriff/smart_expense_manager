// NOT backed by Python yet. Forward-looking contract based on the product spec.

export interface FinancialGoal {
  id: number;
  name: string;
  target_amount: number;
  current_amount: number;
  target_date: string; // ISO date
}

export interface FinancialGoalWithProgress extends FinancialGoal {
  remaining: number;
  percentComplete: number;
}

export type NewFinancialGoal = Omit<FinancialGoal, 'id' | 'current_amount'> & {
  current_amount?: number;
};
export type UpdateFinancialGoal = Partial<Omit<FinancialGoal, 'id'>>;
