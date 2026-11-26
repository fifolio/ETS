export function formatDate(value: string | null, emptyText = "", timeZone?: string): string {
  if (!value) {
    return emptyText;
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return emptyText;
  }
  return new Intl.DateTimeFormat("en-US", { dateStyle: "medium", timeZone }).format(date);
}