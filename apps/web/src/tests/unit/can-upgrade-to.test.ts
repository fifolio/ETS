import { describe, expect, it } from "vitest";

import { canUpgradeTo } from "@/lib/plans/can-upgrade-to";

describe("canUpgradeTo", () => {
    it.each([
        ["explore", "nextmove", true],
        ["explore", "urgent", true],
        ["nextmove", "urgent", true],
        ["urgent", "nextmove", false],
        ["nextmove", "nextmove", false],
        ["nextmove", "explore", false],
    ] as const)("from %s to %s is %s", (current, target, expected) => {
        expect(canUpgradeTo(current, target)).toBe(expected);
    });
});