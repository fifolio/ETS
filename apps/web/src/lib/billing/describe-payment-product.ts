const LABELS: Record<string, string> = {
  plan_nextmove: "Next Move plan",
  plan_urgent: "Urgent plan",
  topup: "Credit top-up",
};

export function describePaymentProduct(sku: string): string {
  return LABELS[sku] ?? sku;
}