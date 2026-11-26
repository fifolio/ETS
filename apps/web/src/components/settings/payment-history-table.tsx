import { describePaymentProduct } from "@/lib/billing/describe-payment-product";
import { describePaymentStatus } from "@/lib/billing/describe-payment-status";
import { formatPaymentAmount } from "@/lib/billing/format-payment-amount";
import { formatDateTime } from "@/lib/format/format-date-time";
import type { PaymentHistoryTableProps } from "@/types/billing";

export function PaymentHistoryTable({ entries }: PaymentHistoryTableProps) {
  return (
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>What</th>
          <th>Amount</th>
          <th>Credits</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {entries.map((entry, index) => (
          <tr key={`${entry.paid_at}-${index}`}>
            <td>{formatDateTime(entry.paid_at, "")}</td>
            <td>{describePaymentProduct(entry.sku)}</td>
            <td>{formatPaymentAmount(entry.amount_cents)}</td>
            <td>{entry.credits > 0 ? entry.credits : "-"}</td>
            <td>{describePaymentStatus(entry.status)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}