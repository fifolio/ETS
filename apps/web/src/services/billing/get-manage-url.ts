import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";

export async function getManageUrl(): Promise<string> {
  const response = await apiFetch("/subscription/manage-url");
  if (!response.ok) {
    throw await readApiError(response);
  }
  const body: { url: string } = await response.json();
  return body.url;
}