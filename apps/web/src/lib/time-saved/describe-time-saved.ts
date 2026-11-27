import { calculateMinutesSaved } from "@/lib/time-saved/calculate-minutes-saved";
import { formatDuration } from "@/lib/time-saved/format-duration";
import type { TimeSavedConfig } from "@/types/time-saved";

export function describeTimeSaved(credits: number, config: TimeSavedConfig, perMonth: boolean): string {
  const duration = formatDuration(calculateMinutesSaved(credits, config));
  const text = `Saves about ${duration} of evaluation time`;
  return perMonth ? `${text} per month` : text;
}