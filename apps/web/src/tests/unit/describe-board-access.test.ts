import { describe, expect, it } from "vitest";

import { describeBoardAccess } from "@/lib/job-boards/describe-board-access";

const indeed = {
    id: "indeed",
    name: "Indeed",
    url: "https://www.indeed.com",
    plan: "nextmove",
    plan_name: "Next Move",
};

describe("describeBoardAccess", () => {
    it("says Available when the plan includes the board", () => {
        expect(describeBoardAccess(indeed, true)).toBe("Available");
    });

    it("names the plan that includes the board when the user's plan doesn't", () => {
        expect(describeBoardAccess(indeed, false)).toBe("Next Move");
    });

    it("works for the top plan too", () => {
        expect(describeBoardAccess({ ...indeed, plan: "urgent", plan_name: "Urgent" }, false)).toBe(
            "Urgent",
        );
    });
});