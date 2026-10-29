import { clearApiToken } from "@/lib/api/clear-api-token";
import { getToken } from "@/lib/api/get-token";
import { sendRequest } from "@/lib/api/send-request";

/** Call the ETS API as the logged-in user. Retries once with a fresh token on a 401. */
export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  let response = await sendRequest(path, init, await getToken());
  if (response.status === 401) {
    clearApiToken();
    response = await sendRequest(path, init, await getToken());
  }
  return response;
}