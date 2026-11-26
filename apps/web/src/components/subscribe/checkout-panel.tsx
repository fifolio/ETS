"use client";

import Link from "next/link";
import { useState } from "react";

import { PaymentResultMessage } from "@/components/settings/payment-result-message";
import { useCheckout } from "@/hooks/use-checkout";
import { usePaymentResult } from "@/hooks/use-payment-result";
import { formatUsd } from "@/lib/topup/format-usd";
import type { CheckoutPanelProps } from "@/types/checkout";

import { WhopCheckout } from "./whop-checkout";

export function CheckoutPanel({ product, amountUsd }: CheckoutPanelProps) {
  const { session, error } = useCheckout(product, amountUsd);
  const [paid, setPaid] = useState(false);
  const paymentResult = usePaymentResult(paid);

  if (paid) {
    return (
      <div>
        <h2>Payment received</h2>
        <PaymentResultMessage state={paymentResult} />
        <Link href="/settings">Back to Settings</Link>
      </div>
    );
  }
  return (
    <div>
      {error && <p role="alert">{error}</p>}
      {!session && !error && <p>Preparing your secure payment...</p>}
      {session && (
        <>
          <p>
            Total: {formatUsd(session.amount_cents)}. Adds {session.credits} credits
            {product === "topup" ? "" : " each month"}.
          </p>
          <WhopCheckout
            session={session}
            returnUrl={`${window.location.origin}/settings?payment=success`}
            onComplete={() => setPaid(true)}
          />
          <p>
            Trouble with the form?{" "}
            <a href={session.checkout_url}>Open the secure payment page</a>.
          </p>
        </>
      )}
      <p>
        <Link href="/settings">Cancel</Link>
      </p>
    </div>
  );
}
