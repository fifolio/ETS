import { describe, expect, it } from "vitest";

import { formatCreditChange } from "@/lib/billing/format-credit-change";
import { formatPaymentAmount } from "@/lib/billing/format-payment-amount";
import { formatDate } from "@/lib/format/format-date";

describe("formatCreditChange", () => {
  it("puts a plus in front of credits that were added", () => {
    expect(formatCreditChange(25)).toBe("+25");
  });

  it("shows credits that were used with their minus", () => {
    expect(formatCreditChange(-1)).toBe("-1");
  });

  it("shows zero as it is", () => {
    expect(formatCreditChange(0)).toBe("0");
  });
});

describe("formatPaymentAmount", () => {
  it("shows an amount in dollars", () => {
    expect(formatPaymentAmount(525)).toBe("$5.25");
  });

  it("shows a dash when no amount was recorded", () => {
    expect(formatPaymentAmount(0)).toBe("-");
  });
});

describe("formatDate", () => {
  it("shows a date without the time", () => {
    expect(formatDate("2026-12-31T23:30:00+00:00", "", "UTC")).toBe("Dec 31, 2026");
  });

  it("shows the given text when there is no date or it isn't one", () => {
    expect(formatDate(null, "none")).toBe("none");
    expect(formatDate("not a date", "none")).toBe("none");
  });
});