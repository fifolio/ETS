import type { TimeSavedConfig, TimeSavedResponse } from "@/types/time-saved";

/** The plans endpoint is public, so this works without a session. */
export async function getTimeSavedConfig(): Promise<TimeSavedConfig> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/plans`);
  if (!response.ok) {
    throw new Error(`The API answered with status ${response.status}.`);
  }
  const body: TimeSavedResponse = await response.json();
  return body.time_saved;
}