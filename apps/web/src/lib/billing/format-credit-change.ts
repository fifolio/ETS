export function formatCreditChange(amount: number): string {
  return amount > 0 ? `+${amount}` : String(amount);
}