import type { SubscriptionPlan } from "@/types/account";

export interface SubscriptionStatus {
  plan: SubscriptionPlan;
  plan_name: string;
  is_paid: boolean;
  current_period_end: string | null;
  cancel_at_period_end: boolean;
  can_manage: boolean;
  can_cancel: boolean;
}

export interface CreditEntry {
  amount: number;
  kind: string;
  reason: string;
  created_at: string | null;
}

export interface PaymentEntry {
  sku: string;
  amount_cents: number;
  credits: number;
  status: string;
  paid_at: string | null;
}

export type PaymentResultState = "idle" | "waiting" | "done" | "problem" | "slow";

export interface SubscriptionDetailsProps {
  status: SubscriptionStatus;
}

export interface CreditHistoryTableProps {
  entries: CreditEntry[];
}

export interface PaymentHistoryTableProps {
  entries: PaymentEntry[];
}

export interface PaymentResultMessageProps {
  state: PaymentResultState;
}