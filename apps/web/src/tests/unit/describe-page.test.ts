import { describe, expect, it } from "vitest";

import { describePage } from "@/lib/billing/describe-page";

describe("describePage", () => {
  it("says nothing when there are no results", () => {
    expect(describePage(1, 1, 0)).toBe("");
  });

  it("shows the page, the number of pages, and the total", () => {
    expect(describePage(2, 5, 47)).toBe("Page 2 of 5 (47 in total)");
  });

  it("works for a single page", () => {
    expect(describePage(1, 1, 3)).toBe("Page 1 of 1 (3 in total)");
  });
});