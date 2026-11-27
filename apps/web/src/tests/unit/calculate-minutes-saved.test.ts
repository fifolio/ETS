import { describe, expect, it } from "vitest";

import { calculateMinutesSaved } from "@/lib/time-saved/calculate-minutes-saved";

const config = { minutes_per_scan: 5, credits_per_scan: 1 };

describe("calculateMinutesSaved", () => {
  it.each([
    [15, 75],
    [150, 750],
    [300, 1500],
    [40, 200],
    [400, 2000],
  ])("%i credits save %i minutes", (credits, minutes) => {
    expect(calculateMinutesSaved(credits, config)).toBe(minutes);
  });

  it("counts scans, not credits, when a scan costs more than one credit", () => {
    expect(calculateMinutesSaved(10, { minutes_per_scan: 5, credits_per_scan: 2 })).toBe(25);
  });

  it("rounds to whole minutes", () => {
    expect(calculateMinutesSaved(3, { minutes_per_scan: 2.5, credits_per_scan: 1 })).toBe(8);
  });

  it("is zero without credits or with an invalid cost per scan", () => {
    expect(calculateMinutesSaved(0, config)).toBe(0);
    expect(calculateMinutesSaved(10, { minutes_per_scan: 5, credits_per_scan: 0 })).toBe(0);
  });
});