import { describeCreditKind } from "@/lib/billing/describe-credit-kind";
import { formatCreditChange } from "@/lib/billing/format-credit-change";
import { formatDateTime } from "@/lib/format/format-date-time";
import type { CreditHistoryTableProps } from "@/types/billing";

export function CreditHistoryTable({ entries }: CreditHistoryTableProps) {
  return (
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Change</th>
          <th>Type</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        {entries.map((entry, index) => (
          <tr key={`${entry.created_at}-${index}`}>
            <td>{formatDateTime(entry.created_at, "")}</td>
            <td>{formatCreditChange(entry.amount)}</td>
            <td>{describeCreditKind(entry.kind)}</td>
            <td>{entry.reason}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}