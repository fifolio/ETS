"use client";

import Link from "next/link";

import { useCheckout } from "@/hooks/use-checkout";
import { formatUsd } from "@/lib/topup/format-usd";
import type { CheckoutPanelProps } from "@/types/checkout";

import { WhopCheckout } from "./whop-checkout";

export function CheckoutPanel({ product, amountUsd }: CheckoutPanelProps) {
  const { session, error } = useCheckout(product, amountUsd);
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
            returnUrl={`${window.location.origin}/settings?payment_result=success`}
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
