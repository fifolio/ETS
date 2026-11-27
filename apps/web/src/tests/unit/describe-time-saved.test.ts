import { describe, expect, it } from "vitest";

import { describeTimeSaved } from "@/lib/time-saved/describe-time-saved";

const config = { minutes_per_scan: 5, credits_per_scan: 1 };

describe("describeTimeSaved", () => {
  it("describes a monthly plan", () => {
    expect(describeTimeSaved(150, config, true)).toBe(
      "Saves about 12 h 30 min of evaluation time per month",
    );
  });

  it("describes a top-up without a period", () => {
    expect(describeTimeSaved(40, config, false)).toBe("Saves about 3 h 20 min of evaluation time");
  });

  it("follows the credits of the slider", () => {
    expect(describeTimeSaved(58, config, false)).toBe("Saves about 4 h 50 min of evaluation time");
  });
});