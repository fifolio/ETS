import { useEffect, useState } from "react";

import { getTimeSavedConfig } from "@/services/time-saved/get-time-saved-config";
import type { TimeSavedConfig } from "@/types/time-saved";

let pending: Promise<TimeSavedConfig> | null = null;

/** One request is shared by every plan card and the top-up page. A failure can be retried. */
function loadOnce(): Promise<TimeSavedConfig> {
  if (!pending) {
    pending = getTimeSavedConfig().catch((error) => {
      pending = null;
      throw error;
    });
  }
  return pending;
}

export function useTimeSavedConfig(): TimeSavedConfig | null {
  const [config, setConfig] = useState<TimeSavedConfig | null>(null);

  useEffect(() => {
    let current = true;
    loadOnce()
      .then((loaded) => current && setConfig(loaded))
      .catch(() => {
        // the time saved is a nice-to-have: without it the line is left out
      });
    return () => {
      current = false;
    };
  }, []);

  return config;
}