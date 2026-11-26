const LABELS: Record<string, string> = {
  completed: "Paid",
  failed: "Failed",
  underpaid: "Underpaid: not applied",
  refunded: "Refunded",
  pending: "Pending",
};

export function describePaymentStatus(status: string): string {
  return LABELS[status] ?? status;
}