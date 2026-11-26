import { formatUsd } from "@/lib/topup/format-usd";

/** A payment that never got an amount (a failed one nobody recorded) shows a dash. */
export function formatPaymentAmount(cents: number): string {
  return cents > 0 ? formatUsd(cents) : "-";
}