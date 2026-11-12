export function describeJobBoards(max: number | null): string {
    if (max === null) {
        return "All job boards";
    }
    return max === 1 ? "1 job board" : `Up to ${max} job boards`;
}