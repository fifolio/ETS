import { ApiRequestError } from "@/lib/api/api-request-error";

export function describeUploadError(error: unknown): string[] {
    if (error instanceof ApiRequestError) {
        return error.problems.length > 0 ? error.problems : [error.message];
    }
    return ["Could not upload the CV. Is the API running?"];
}