import { describe, expect, it } from "vitest";

import { describePaymentResult } from "@/lib/billing/describe-payment-result";

describe("describePaymentResult", () => {
  it("says it is confirming while waiting", () => {
    expect(describePaymentResult("waiting")).toMatch(/confirming/);
  });

  it("says the payment was confirmed when done", () => {
    expect(describePaymentResult("done")).toMatch(/confirmed/);
  });

  it("points to support when the payment could not be applied", () => {
    expect(describePaymentResult("problem")).toMatch(/support/);
  });

  it("explains a slow confirmation and says nothing when idle", () => {
    expect(describePaymentResult("slow")).toMatch(/longer than usual/);
    expect(describePaymentResult("idle")).toBe("");
  });
});