export async function sendRequest(
  path: string,
  init: RequestInit,
  token: string,
): Promise<Response> {
  const headers = new Headers(init.headers);
  headers.set("Authorization", `Bearer ${token}`);
  const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  return fetch(`${baseUrl}${path}`, { ...init, headers });
}