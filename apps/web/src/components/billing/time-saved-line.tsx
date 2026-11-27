"use client";

import { useTimeSavedConfig } from "@/hooks/use-time-saved-config";
import { describeTimeSaved } from "@/lib/time-saved/describe-time-saved";
import type { TimeSavedLineProps } from "@/types/time-saved";

export function TimeSavedLine({ credits, perMonth = false }: TimeSavedLineProps) {
  const config = useTimeSavedConfig();

  if (!config) {
    return null;
  }
  return <span>{describeTimeSaved(credits, config, perMonth)}</span>;
}