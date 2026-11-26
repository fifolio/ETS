import { formatDate } from "@/lib/format/format-date";
import type { SubscriptionStatus } from "@/types/billing";

export function describeRenewal(status: SubscriptionStatus, timeZone?: string): string {
  if (!status.is_paid) {
    return "Free plan: no renewal.";
  }
  const date = formatDate(status.current_period_end, "", timeZone);
  if (status.cancel_at_period_end) {
    return date ? `Cancelled: your plan ends on ${date}.` : "Cancelled: your plan ends at the end of the period.";
  }
  return date ? `Renews on ${date}.` : "Active.";
}