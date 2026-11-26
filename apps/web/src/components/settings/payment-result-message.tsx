import { describePaymentResult } from "@/lib/billing/describe-payment-result";
import type { PaymentResultMessageProps } from "@/types/billing";

export function PaymentResultMessage({ state }: PaymentResultMessageProps) {
  const text = describePaymentResult(state);
  if (!text) {
    return null;
  }
  return <p role={state === "problem" ? "alert" : "status"}>{text}</p>;
}