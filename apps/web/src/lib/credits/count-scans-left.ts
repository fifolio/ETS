export function countScansLeft(total: number, creditsPerScan: number): number {
    return creditsPerScan > 0 ? Math.floor(total / creditsPerScan) : 0;
}