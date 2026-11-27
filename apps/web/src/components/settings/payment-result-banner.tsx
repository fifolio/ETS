"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";

import { usePaymentResult } from "@/hooks/use-payment-result";

import { PaymentResultMessage } from "./payment-result-message";

/** Shown when Whop sends the user back to Settings after paying. */
export function PaymentResultBanner() {
  const router = useRouter();
  const params = useSearchParams();
  const query = params.toString();
  const returned =
    params.get("payment_result") === "success" || params.get("payment") === "success";
  const state = usePaymentResult(returned);

  useEffect(() => {
    if (returned && query !== "payment_result=success") {
      router.replace("/settings?payment_result=success");
    }
  }, [query, returned, router]);

  if (!returned) {
    return null;
  }
  return (
    <section>
      <PaymentResultMessage state={state} />
    </section>
  );
}