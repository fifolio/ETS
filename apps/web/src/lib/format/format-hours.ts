export function formatHours(value: number): string {
    const totalMinutes = Math.max(0, Math.round(value * 60));
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;

    return `${hours}h ${minutes}m`;
}