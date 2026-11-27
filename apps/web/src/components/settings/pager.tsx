import type { PagerProps } from "@/types/pagination";

export function Pager({ page, totalPages, onPage }: PagerProps) {
  return (
    <p>
      <button type="button" onClick={() => onPage(page - 1)} disabled={page <= 1}>
        Previous
      </button>{" "}
      <button type="button" onClick={() => onPage(page + 1)} disabled={page >= totalPages}>
        Next
      </button>
    </p>
  );
}