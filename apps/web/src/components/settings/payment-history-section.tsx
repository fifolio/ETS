"use client";

import { usePaymentHistory } from "@/hooks/use-payment-history";

import { PaymentHistoryTable } from "./payment-history-table";

export function PaymentHistorySection() {
  const { data, error } = usePaymentHistory();

  return (
    <section>
      <h2>Payments</h2>
      {error && <p role="alert">{error}</p>}
      {!data && !error && <p>Loading...</p>}
      {data && data.length === 0 && <p>No payments yet.</p>}
      {data && data.length > 0 && <PaymentHistoryTable entries={data} />}
    </section>
  );
}