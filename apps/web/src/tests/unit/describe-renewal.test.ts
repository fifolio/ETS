import { describe, expect, it } from "vitest";

import { describeRenewal } from "@/lib/billing/describe-renewal";
import type { SubscriptionStatus } from "@/types/billing";

const paid: SubscriptionStatus = {
  plan: "nextmove",
  plan_name: "Next Move",
  is_paid: true,
  current_period_end: "2026-12-31T00:00:00+00:00",
  cancel_at_period_end: false,
  can_manage: true,
  can_cancel: true,
};

describe("describeRenewal", () => {
  it("says the free plan has no renewal", () => {
    expect(describeRenewal({ ...paid, is_paid: false, current_period_end: null }, "UTC")).toBe(
      "Free plan: no renewal.",
    );
  });

  it("shows the renewal date of a paid plan", () => {
    expect(describeRenewal(paid, "UTC")).toBe("Renews on Dec 31, 2026.");
  });

  it("shows when a cancelled plan ends", () => {
    expect(describeRenewal({ ...paid, cancel_at_period_end: true }, "UTC")).toBe(
      "Cancelled: your plan ends on Dec 31, 2026.",
    );
  });

  it("says a paid plan without a date is active", () => {
    expect(describeRenewal({ ...paid, current_period_end: null }, "UTC")).toBe("Active.");
  });

  it("says a cancelled plan without a date ends at the end of the period", () => {
    expect(describeRenewal({ ...paid, current_period_end: null, cancel_at_period_end: true }, "UTC")).toBe(
      "Cancelled: your plan ends at the end of the period.",
    );
  });
});