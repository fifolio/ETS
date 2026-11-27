export function describePage(page: number, totalPages: number, total: number): string {
    return total === 0 ? "" : `Page ${page} of ${totalPages} (${total} in total)`;
}