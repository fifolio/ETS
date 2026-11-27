import type { TimeSavedConfig } from "@/types/time-saved";

/** Credits are scans, and every scan saves the average reading time. Whole minutes. */
export function calculateMinutesSaved(credits: number, config: TimeSavedConfig): number {
  if (credits <= 0 || config.credits_per_scan <= 0) {
    return 0;
  }
  return Math.round((credits / config.credits_per_scan) * config.minutes_per_scan);
}