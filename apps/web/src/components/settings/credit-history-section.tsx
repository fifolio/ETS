"use client";

import { useCreditHistory } from "@/hooks/use-credit-history";
import { describePage } from "@/lib/billing/describe-page";

import { CreditHistoryFilters } from "./credit-history-filters";
import { CreditHistoryTable } from "./credit-history-table";
import { Pager } from "./pager";

export function CreditHistorySection() {
  const { data, error, filters, setPage, changeFilters } = useCreditHistory();

  return (
    <section>
      <h2>Credit history</h2>
      <CreditHistoryFilters filters={filters} onChange={changeFilters} />
      {error && <p role="alert">{error}</p>}
      {!data && !error && <p>Loading...</p>}
      {data && data.items.length === 0 && <p>No credit changes found.</p>}
      {data && data.items.length > 0 && <CreditHistoryTable entries={data.items} />}
      {data && data.total > 0 && (
        <>
          <p>{describePage(data.page, data.total_pages, data.total)}</p>
          <Pager page={data.page} totalPages={data.total_pages} onPage={setPage} />
        </>
      )}
    </section>
  );
}