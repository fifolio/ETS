export interface SiteTotals {
    total_users: number;
    total_scans: number;
    total_minutes_saved: number;
    total_hours_saved: number;
    total_cash_saved_usd: number;
}

export interface SiteTotalsProps {
    totals: SiteTotals;
}