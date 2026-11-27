import { describe, expect, it } from "vitest";

import { buildHistoryQuery } from "@/lib/billing/build-history-query";

describe("buildHistoryQuery", () => {
  it("is only the page when no filter is chosen", () => {
    expect(buildHistoryQuery(1, { kind: "all", change: "all" })).toBe("?page=1");
  });

  it("adds a filter that isn't all", () => {
    expect(buildHistoryQuery(2, { kind: "purchased", change: "all" })).toBe("?page=2&kind=purchased");
  });

  it("adds every filter that isn't all", () => {
    expect(buildHistoryQuery(1, { kind: "purchased", change: "used" })).toBe("?page=1&kind=purchased&change=used");
  });

  it("works for the payment filters", () => {
    expect(buildHistoryQuery(3, { status: "failed", product: "all" })).toBe("?page=3&status=failed");
  });
});