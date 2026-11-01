import { describe, expect, it } from "vitest";

import { readApiError } from "@/lib/api/read-api-error";

describe("readApiError", () => {
    it("reads the message and the list of problems from the API's JSON error", async () => {
        const body = { detail: "The CV did not pass validation.", problems: ["No email found."] };
        const error = await readApiError(new Response(JSON.stringify(body), { status: 422 }));

        expect(error.status).toBe(422);
        expect(error.message).toBe("The CV did not pass validation.");
        expect(error.problems).toEqual(["No email found."]);
    });

    it("falls back to the status code when the body isn't JSON", async () => {
        const error = await readApiError(new Response("Bad gateway", { status: 502 }));

        expect(error.message).toBe("The API answered with status 502.");
        expect(error.problems).toEqual([]);
    });
});