/** Dollars typed by a person ("5", "5.25", "$5,25") as cents, or null when it isn't an amount. */
export function parseAmountText(text: string): number | null {
  const cleaned = text.trim().replace(/^\$/, "").replace(",", ".");
  if (!/^\d+(\.\d{1,2})?$/.test(cleaned)) {
    return null;
  }
  return Math.round(Number(cleaned) * 100);
}