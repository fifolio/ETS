import { getApiBaseUrl } from "@/lib/api/get-api-base-url";


export async function sendRequest(
  path: string,
  init: RequestInit,
  token: string,
): Promise<Response> {
  const headers = new Headers(init.headers);
  headers.set("Authorization", `Bearer ${token}`);
  return fetch(`${getApiBaseUrl()}${path}`, { ...init, headers });
}