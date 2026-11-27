import { describe, expect, it } from "vitest";

import { formatDuration } from "@/lib/time-saved/format-duration";

describe("formatDuration", () => {
  it.each([
    [0, "0 min"],
    [45, "45 min"],
    [60, "1 h"],
    [61, "1 h 1 min"],
    [750, "12 h 30 min"],
    [1500, "25 h"],
  ])("%i minutes is %s", (minutes, text) => {
    expect(formatDuration(minutes)).toBe(text);
  });

  it("never goes below zero", () => {
    expect(formatDuration(-5)).toBe("0 min");
  });
});