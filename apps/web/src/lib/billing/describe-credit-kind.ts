const LABELS: Record<string, string> = {
  subscription: "Monthly allowance",
  promotional: "Welcome bonus",
  purchased: "Purchased",
};

export function describeCreditKind(kind: string): string {
  return LABELS[kind] ?? kind;
}