import { describe, expect, it } from "vitest";

import {
  CREDIT_CHANGE_OPTIONS,
  CREDIT_KIND_OPTIONS,
  DEFAULT_CREDIT_FILTERS,
  DEFAULT_PAYMENT_FILTERS,
  PAYMENT_PRODUCT_OPTIONS,
  PAYMENT_STATUS_OPTIONS,
} from "@/lib/billing/history-filter-options";

const lists = [CREDIT_KIND_OPTIONS, CREDIT_CHANGE_OPTIONS, PAYMENT_STATUS_OPTIONS, PAYMENT_PRODUCT_OPTIONS];

describe("history filter options", () => {
  it("start with all, and every value is unique", () => {
    for (const options of lists) {
      expect(options[0].value).toBe("all");
      expect(new Set(options.map((option) => option.value)).size).toBe(options.length);
    }
  });

  it("have defaults that mean no filtering", () => {
    expect(Object.values(DEFAULT_CREDIT_FILTERS)).toEqual(["all", "all"]);
    expect(Object.values(DEFAULT_PAYMENT_FILTERS)).toEqual(["all", "all"]);
  });
});