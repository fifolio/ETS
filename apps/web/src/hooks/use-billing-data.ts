import { useEffect, useState } from "react";

import { useBillingStore } from "@/stores/billing/billing-store";

/** Loads billing data and loads it again whenever the billing version changes. */
export function useBillingData<T>(load: () => Promise<T>, failureText: string) {
  const version = useBillingStore((state) => state.version);
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let current = true;
    load()
      .then((result) => {
        if (current) {
          setData(result);
          setError("");
        }
      })
      .catch((err) => {
        if (current) {
          setError(err instanceof Error ? err.message : failureText);
        }
      });
    return () => {
      current = false;
    };
  }, [version, load, failureText]);

  return { data, error };
}