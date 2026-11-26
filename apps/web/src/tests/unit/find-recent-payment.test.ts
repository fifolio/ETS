import { describe, expect, it } from "vitest";

import { findRecentPayment } from "@/lib/billing/find-recent-payment";
import type { PaymentEntry } from "@/types/billing";

const NOW = Date.parse("2026-12-01T12:00:00Z");
const WINDOW = 10 * 60 * 1000;

const entry = (paid_at: string | null, status = "completed"): PaymentEntry => ({
  sku: "topup",
  amount_cents: 500,
  credits: 40,
  status,
  paid_at,
});

describe("findRecentPayment", () => {
  it("finds a payment from the last few minutes", () => {
    const recent = entry("2026-12-01T11:58:00Z");

    expect(findRecentPayment([recent], NOW, WINDOW)).toBe(recent);
  });

  it("ignores a payment older than the window", () => {
    expect(findRecentPayment([entry("2026-12-01T11:00:00Z")], NOW, WINDOW)).toBeNull();
  });

  it("returns the newest recent payment first", () => {
    const newest = entry("2026-12-01T11:59:00Z", "failed");

    expect(findRecentPayment([newest, entry("2026-12-01T11:55:00Z")], NOW, WINDOW)).toBe(newest);
  });

  it("ignores payments without a readable date", () => {
    expect(findRecentPayment([entry(null), entry("nonsense")], NOW, WINDOW)).toBeNull();
  });
});