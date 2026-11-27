"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect } from "react";

import { CheckoutPanel } from "@/components/subscribe/checkout-panel";
import { TopupPicker } from "@/components/subscribe/topup-picker";
import { usePlans } from "@/hooks/use-plans";
import { describeProduct } from "@/lib/checkout/describe-product";
import { parseProduct } from "@/lib/checkout/parse-product";
import { parseAmountText } from "@/lib/topup/parse-amount-text";

function SubscribeContent() {
  const router = useRouter();
  const params = useSearchParams();
  const paymentSucceeded = params.get("payment") === "success";
  const product = parseProduct(params.get("product"));
  const { topup, error } = usePlans();

  useEffect(() => {
    if (paymentSucceeded) {
      router.replace("/settings?payment=success");
    }
  }, [paymentSucceeded, router]);

  if (!product) {
    return (
      <main>
        <h1>Checkout</h1>
        <p>Choose a plan or buy credits in Settings.</p>
        <Link href="/settings">Go to Settings</Link>
      </main>
    );
  }
  if (product === "topup") {
    const cents = parseAmountText(params.get("amount") ?? "");
    if (cents === null) {
      return (
        <main>
          <h1>Buy credits</h1>
          {error && <p role="alert">{error}</p>}
          {!topup && !error && <p>Loading...</p>}
          {topup && (
            <TopupPicker
              config={topup}
              onContinue={(chosen) =>
                router.push(
                  `/subscribe?product=topup&amount=${(chosen / 100).toFixed(2)}`,
                )
              }
            />
          )}
          <p>
            <Link href="/settings">Cancel</Link>
          </p>
        </main>
      );
    }
    return (
      <main>
        <h1>Checkout</h1>
        <p>{describeProduct(product)}</p>
        <CheckoutPanel product={product} amountUsd={cents / 100} />
      </main>
    );
  }
  return (
    <main>
      <h1>Checkout</h1>
      <p>{describeProduct(product)}</p>
      <CheckoutPanel product={product} />
    </main>
  );
}

export default function SubscribePage() {
  return (
    <Suspense>
      <SubscribeContent />
    </Suspense>
  );
}
