import type { PaymentResultState } from "@/types/billing";

export function describePaymentResult(state: PaymentResultState): string {
  switch (state) {
    case "waiting":
      return "We are confirming your payment. This usually takes a few seconds.";
    case "done":
      return "Your payment was confirmed. Your plan and credits are updated.";
    case "problem":
      return "Your payment could not be applied. If you were charged, please contact support.";
    case "slow":
      return "Confirmation is taking longer than usual. It will appear in your payment history shortly.";
    default:
      return "";
  }
}