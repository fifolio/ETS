import { describe, expect, it } from "vitest";

import { describeJobBoards } from "@/lib/plans/describe-job-boards";

describe("describeJobBoards", () => {
    it("describes a single job board", () => {
        expect(describeJobBoards(1)).toBe("1 job board");
    });

    it("describes a limit", () => {
        expect(describeJobBoards(3)).toBe("Up to 3 job boards");
    });

    it("describes no limit", () => {
        expect(describeJobBoards(null)).toBe("All job boards");
    });
});