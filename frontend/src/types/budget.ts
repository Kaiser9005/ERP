export interface Budget {
  category: string;
  spent: number;
  allocated: number;
}

export interface BudgetOverviewData {
  budgets: Budget[];
  totalSpent: number;
  totalAllocated: number;
}
