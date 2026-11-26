import { useEffect, useState } from "react";

import { findRecentPayment } from "@/lib/billing/find-recent-payment";
import { getPaymentHistory } from "@/services/billing/get-payment-history";
import { useAuthStore } from "@/stores/auth/auth-store";
import { useBillingStore } from "@/stores/billing/billing-store";
import type { PaymentResultState } from "@/types/billing";

const POLL_MS = 3000;
const MAX_TRIES = 15;
const RECENT_PAYMENT_MS = 10 * 60 * 1000;

/** After paying: waits for the webhook to record the payment, then refreshes the billing screens. */
export function usePaymentResult(enabled: boolean): PaymentResultState {
  const refresh = useAuthStore((state) => state.refresh);
  const bump = useBillingStore((state) => state.bump);
  const [state, setState] = useState<PaymentResultState>("idle");

  useEffect(() => {
    if (!enabled) {
      return;
    }
    let cancelled = false;
    let tries = 0;
    const timer = setInterval(async () => {
      tries += 1;
      try {
        const payment = findRecentPayment(await getPaymentHistory(), Date.now(), RECENT_PAYMENT_MS);
        if (cancelled) {
          return;
        }
        if (payment) {
          clearInterval(timer);
          if (payment.status === "completed") {
            await refresh(); // the plan label may have changed
            bump();
            setState("done");
          } else {
            setState("problem");
          }
          return;
        }
      } catch {
        // try again on the next tick
      }
      if (tries >= MAX_TRIES && !cancelled) {
        clearInterval(timer);
        setState("slow");
      }
    }, POLL_MS);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [enabled, refresh, bump]);

  return enabled ? (state === "idle" ? "waiting" : state) : "idle";
}