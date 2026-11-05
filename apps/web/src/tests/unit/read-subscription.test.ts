import { describe, expect, it } from "vitest";

import { readSubscription } from "@/lib/account/read-subscription";
import type { AppUser } from "@/types/auth/auth";

const makeUser = (labels: string[]) => ({ labels }) as unknown as AppUser;

describe("readSubscription", () => {
    it("is free when the user has no plan label", () => {
        expect(readSubscription(makeUser([]))).toBe("explore");
    });

    it("reads a plan label", () => {
        expect(readSubscription(makeUser(["cvdone", "nextmove"]))).toBe("nextmove");
    });

    it("uses the highest plan when there are several", () => {
        expect(readSubscription(makeUser(["nextmove", "urgent"]))).toBe("urgent");
    });
});