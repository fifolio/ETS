"use client";

import { usePaymentHistory } from "@/hooks/use-payment-history";
import { describePage } from "@/lib/billing/describe-page";

import { Pager } from "./pager";
import { PaymentHistoryFilters } from "./payment-history-filters";
import { PaymentHistoryTable } from "./payment-history-table";

export function PaymentHistorySection() {
  const { data, error, filters, setPage, changeFilters } = usePaymentHistory();

  return (
    <section>
      <h2>Payments</h2>
      <PaymentHistoryFilters filters={filters} onChange={changeFilters} />
      {error && <p role="alert">{error}</p>}
      {!data && !error && <p>Loading...</p>}
      {data && data.items.length === 0 && <p>No payments found.</p>}
      {data && data.items.length > 0 && <PaymentHistoryTable entries={data.items} />}
      {data && data.total > 0 && (
        <>
          <p>{describePage(data.page, data.total_pages, data.total)}</p>
          <Pager page={data.page} totalPages={data.total_pages} onPage={setPage} />
        </>
      )}
    </section>
  );
}