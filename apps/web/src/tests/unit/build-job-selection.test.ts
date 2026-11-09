import { describe, expect, it } from "vitest";

import { buildJobSelection } from "@/lib/catalog/build-job-selection";

const industries = [{ id: "marketing", name: "Marketing & Advertising" }];
const jobs = [{ id: "job-1", name: "SEO Specialist", hourly_rate_usd: 35 }];

describe("buildJobSelection", () => {
    it("builds the saved choice from the picked industry and role", () => {
        expect(buildJobSelection(industries, jobs, "marketing", "job-1")).toEqual({
            industryId: "marketing",
            industry: "Marketing & Advertising",
            jobId: "job-1",
            role: "SEO Specialist",
            hourlyRateUsd: 35,
        });
    });

    it("returns null when the industry is unknown", () => {
        expect(buildJobSelection(industries, jobs, "other", "job-1")).toBeNull();
    });

    it("returns null when the role isn't in the list", () => {
        expect(buildJobSelection(industries, jobs, "marketing", "job-9")).toBeNull();
    });
});