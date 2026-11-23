"use client";

import { useCredits } from "@/hooks/use-credits";
import { countScansLeft } from "@/lib/credits/count-scans-left";
import { TopUpButton } from "./top-up-button";

export function CreditsSection() {
  const { credits, error } = useCredits();

  return (
    <section>
      <h2>Credits</h2>
      {error && <p role="alert">{error}</p>}
      {!credits && !error && <p>Loading...</p>}
      {credits && (
        <>
          <p>
            {credits.total} credits (about{" "}
            {countScansLeft(credits.total, credits.credits_per_scan)} scans)
          </p>
          <ul>
            <li>Monthly allowance: {credits.subscription}</li>
            <li>Welcome bonus: {credits.promotional}</li>
            <li>Purchased: {credits.purchased}</li>
          </ul>
          <p>
            Credits are used in this order: monthly allowance, welcome bonus,
            purchased. The monthly allowance resets each billing period and
            doesn&apos;t roll over. The welcome bonus (25 credits, granted once per
            account) and purchased credits don&apos;t expire. A scan costs{" "}
            {credits.credits_per_scan} credit, and a job page you already
            scanned costs nothing.
          </p>
          <TopUpButton />
        </>
      )}
    </section>
  );
}
