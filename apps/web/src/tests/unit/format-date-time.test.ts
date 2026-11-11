import { describe, expect, it } from "vitest";

import { formatDateTime } from "@/lib/format/format-date-time";

describe("formatDateTime", () => {
    it("formats an ISO date for people", () => {
        const text = formatDateTime("2026-11-11T12:00:00+00:00", "Unknown", "UTC");

        expect(text).toMatch(/Nov 11, 2026/);
        expect(text).toMatch(/12:00/);
    });

    it("shows the given text when there is no date", () => {
        expect(formatDateTime(null, "Never")).toBe("Never");
    });

    it("shows Unknown for something that isn't a date", () => {
        expect(formatDateTime("not a date")).toBe("Unknown");
    });
});