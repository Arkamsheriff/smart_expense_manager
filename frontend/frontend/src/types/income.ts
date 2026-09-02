// NOT backed by Python yet. This is a forward-looking contract based on the product spec,
// not a real backend schema. Field names may need to change once app/income/ exists.

export interface Income {
  id: number;
  source: string;
  amount: number;
  category: string;
  received_at: string; // ISO datetime string
  notes?: string;
}

export type NewIncome = Omit<Income, 'id'>;
export type UpdateIncome = Partial<NewIncome>;

export interface IncomeCategoryTotal {
  category: string;
  total: number;
}
