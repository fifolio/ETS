import { useEffect, useState } from "react";

import { cancelSubscription } from "@/services/billing/cancel-subscription";
import { getManageUrl } from "@/services/billing/get-manage-url";

export function useSubscriptionActions(canManage: boolean) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [manageUrl, setManageUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!canManage) {
      return;
    }

    let cancelled = false;
    getManageUrl()
      .then((url) => {
        if (!cancelled) {
          setManageUrl(url);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Could not open the billing page.");
        }
      });

    return () => {
      cancelled = true;
    };
  }, [canManage]);

  async function cancel() {
    if (!window.confirm(
      "Cancel your subscription now? Your paid access and unused plan credits will end immediately. There is no prorated refund, and you can purchase the plan again right away."
    )) {
      return;
    }
    setBusy(true);
    setError("");
    try {
      await cancelSubscription();
      window.history.replaceState(window.history.state, "", window.location.pathname);
      window.location.reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not cancel the subscription.");
    } finally {
      setBusy(false);
    }
  }

  return { busy, error, manageUrl, cancel };
}