"use client";

import Link from "next/link";

import { usePlans } from "@/hooks/use-plans";
import { describeRate } from "@/lib/topup/describe-rate";

export function TopUpButton() {
  const { topup, paymentsEnabled } = usePlans();

  if (!topup) {
    return null;
  }
  const label = `Buy credits (${describeRate(topup)})`;
  return paymentsEnabled ? (
    <Link href="/subscribe?product=topup">{label}</Link>
  ) : (
    <button type="button" disabled>
      {label} (opens soon)
    </button>
  );
}
