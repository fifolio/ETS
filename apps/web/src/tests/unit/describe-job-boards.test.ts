import { describe, expect, it } from "vitest";

import { describeJobBoards } from "@/lib/plans/describe-job-boards";

describe("describeJobBoards", () => {
    it("describes a single job board", () => {
        expect(describeJobBoards(1)).toBe("1 job board");
    });

    it("describes several job boards", () => {
        expect(describeJobBoards(3)).toBe("3 job boards");
    });

    it("describes a plan with no job boards yet", () => {
        expect(describeJobBoards(0)).toBe("No job boards yet");
    });
});