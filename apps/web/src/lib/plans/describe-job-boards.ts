export function describeJobBoards(count: number): string {
    if (count === 0) {
        return "No job boards yet";
    }
    return count === 1 ? "1 job board" : `${count} job boards`;
}