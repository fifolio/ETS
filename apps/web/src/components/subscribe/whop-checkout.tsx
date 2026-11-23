"use client";

import { loadWhop } from "@whop/elements";
import { Checkout, CheckoutElement, WhopElements } from "@whop/elements-react";

import { getEmbedEnvironment } from "@/lib/checkout/get-embed-environment";
import type { WhopCheckoutProps } from "@/types/checkout";

export function WhopCheckout({
  session,
  returnUrl,
  onComplete,
}: WhopCheckoutProps) {
  return (
    <WhopElements
      elements={loadWhop()}
      environment={getEmbedEnvironment(session.environment)}
    >
      <Checkout
        checkoutConfiguration={session.checkout_id}
        returnUrl={returnUrl}
        onComplete={onComplete}
      >
        <CheckoutElement />
      </Checkout>
    </WhopElements>
  );
}
