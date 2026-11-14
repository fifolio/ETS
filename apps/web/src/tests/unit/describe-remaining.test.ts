import { describe, expect, it } from "vitest";

import { describeRemaining } from "@/lib/job-boards/describe-remaining";

describe("describeRemaining", () => {
    it("says how many suggestions are left", () => {
        expect(describeRemaining(2)).toBe("You can send 2 more suggestions today.");
    });

    it("uses the singular for one", () => {
        expect(describeRemaining(1)).toBe("You can send 1 more suggestion today.");
    });

    it("says when none are left", () => {
        expect(describeRemaining(0)).toBe("You have no suggestions left today.");
    });
});