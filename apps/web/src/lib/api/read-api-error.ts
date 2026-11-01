import { ApiRequestError } from "@/lib/api/api-request-error";
import type { ApiErrorBody } from "@/types/api";

/** Turn a failed API response into an error that carries the status and the list of problems. */
export async function readApiError(response: Response): Promise<ApiRequestError> {
    let body: ApiErrorBody = {};
    try {
        body = await response.json();
    } catch {
        // The body wasn't JSON, so the status code is all we have.
    }
    const message =
        typeof body.detail === "string"
            ? body.detail
            : `The API answered with status ${response.status}.`;
    return new ApiRequestError(response.status, message, body.problems ?? []);
}