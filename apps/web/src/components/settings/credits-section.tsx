"use client";

import { useCredits } from "@/hooks/use-credits";
import { countScansLeft } from "@/lib/credits/count-scans-left";

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
            <li>Bonus: {credits.promotional}</li>
            <li>Monthly allowance: {credits.subscription}</li>
            <li>Purchased: {credits.purchased}</li>
          </ul>
          <p>
            Credits are used in this order: bonus, monthly allowance, purchased.
            Bonus and purchased credits never expire. A scan costs{" "}
            {credits.credits_per_scan} credit, and a job page you already
            scanned costs nothing.
          </p>
        </>
      )}
    </section>
  );
}
