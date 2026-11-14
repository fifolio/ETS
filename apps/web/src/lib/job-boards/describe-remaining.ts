export function describeRemaining(count: number): string {
    if (count <= 0) {
        return "You have no suggestions left today.";
    }
    return count === 1
        ? "You can send 1 more suggestion today."
        : `You can send ${count} more suggestions today.`;
}