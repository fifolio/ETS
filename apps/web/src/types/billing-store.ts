export interface BillingState {
  version: number;
}

export interface BillingActions {
  bump: () => void;
}

export type BillingStore = BillingState & BillingActions;