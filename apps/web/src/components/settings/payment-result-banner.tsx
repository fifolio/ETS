"use client";

import { useSearchParams } from "next/navigation";

import { usePaymentResult } from "@/hooks/use-payment-result";

import { PaymentResultMessage } from "./payment-result-message";

/** Shown when Whop sends the user back to Settings after paying (?payment=success). */
export function PaymentResultBanner() {
  const returned = useSearchParams().get("payment") === "success";
  const state = usePaymentResult(returned);

  if (!returned) {
    return null;
  }
  return (
    <section>
      <PaymentResultMessage state={state} />
    </section>
  );
}