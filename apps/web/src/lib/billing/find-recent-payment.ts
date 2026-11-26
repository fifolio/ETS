import type { PaymentEntry } from "@/types/billing";

/** The newest payment (the list is newest first) that happened within the window, or null. */
export function findRecentPayment(
  entries: PaymentEntry[],
  nowMs: number,
  windowMs: number,
): PaymentEntry | null {
  return (
    entries.find((entry) => {
      const time = entry.paid_at ? new Date(entry.paid_at).getTime() : NaN;
      return !Number.isNaN(time) && nowMs - time <= windowMs;
    }) ?? null
  );
}