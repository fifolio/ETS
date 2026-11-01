import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { CvInfo } from "@/types/cv";

export async function uploadCv(file: File): Promise<CvInfo> {
    const body = new FormData();
    body.append("file", file);
    const response = await apiFetch("/cv", { method: "POST", body });
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}