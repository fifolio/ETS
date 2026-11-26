import { describe, expect, it } from "vitest";

import { describeCreditKind } from "@/lib/billing/describe-credit-kind";
import { describePaymentProduct } from "@/lib/billing/describe-payment-product";
import { describePaymentStatus } from "@/lib/billing/describe-payment-status";

describe("describeCreditKind", () => {
  it.each([
    ["subscription", "Monthly allowance"],
    ["promotional", "Welcome bonus"],
    ["purchased", "Purchased"],
    ["gift", "gift"],
  ])("%s is %s", (kind, label) => {
    expect(describeCreditKind(kind)).toBe(label);
  });
});

describe("describePaymentProduct", () => {
  it.each([
    ["plan_nextmove", "Next Move plan"],
    ["plan_urgent", "Urgent plan"],
    ["topup", "Credit top-up"],
    ["other", "other"],
  ])("%s is %s", (sku, label) => {
    expect(describePaymentProduct(sku)).toBe(label);
  });
});

describe("describePaymentStatus", () => {
  it.each([
    ["completed", "Paid"],
    ["failed", "Failed"],
    ["underpaid", "Underpaid: not applied"],
    ["refunded", "Refunded"],
    ["pending", "Pending"],
  ])("%s is %s", (status, label) => {
    expect(describePaymentStatus(status)).toBe(label);
  });
});