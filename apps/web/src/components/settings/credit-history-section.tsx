"use client";

import { useCreditHistory } from "@/hooks/use-credit-history";

import { CreditHistoryTable } from "./credit-history-table";

export function CreditHistorySection() {
  const { data, error } = useCreditHistory();

  return (
    <section>
      <h2>Credit history</h2>
      {error && <p role="alert">{error}</p>}
      {!data && !error && <p>Loading...</p>}
      {data && data.length === 0 && <p>No credit changes yet.</p>}
      {data && data.length > 0 && <CreditHistoryTable entries={data} />}
    </section>
  );
}