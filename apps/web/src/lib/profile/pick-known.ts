/** Keep only the values that appear in the allowed list. */
export function pickKnown<T extends string>(value: unknown, allowed: readonly T[]): T[] {
    if (!Array.isArray(value)) {
        return [];
    }
    return value.filter((item): item is T => allowed.includes(item));
}