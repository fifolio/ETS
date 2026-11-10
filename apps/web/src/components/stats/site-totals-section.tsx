import { formatCash } from "@/lib/format/format-cash";
import { formatCount } from "@/lib/format/format-count";
import { formatHours } from "@/lib/format/format-hours";
import type { SiteTotalsProps } from "@/types/stats";

export function SiteTotalsSection({ totals }: SiteTotalsProps) {
    return (
        <section>
            <h2>ETS so far</h2>
            <ul>
                <li>{formatCount(totals.total_users)} users</li>
                <li>{formatCount(totals.total_scans)} jobs scanned</li>
                <li>{formatHours(totals.total_hours_saved)} hours saved</li>
                <li>{formatCash(totals.total_cash_saved_usd)} saved</li>
            </ul>
        </section>
    );
}