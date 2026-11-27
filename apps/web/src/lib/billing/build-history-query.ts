/** "?page=2&kind=purchased": only the filters that aren't "all", so the address stays short. */
export function buildHistoryQuery(page: number, filters: object): string {
  const params = new URLSearchParams({ page: String(page) });
  for (const [name, value] of Object.entries(filters)) {
    if (value !== "all") {
      params.set(name, String(value));
    }
  }
  return `?${params.toString()}`;
}