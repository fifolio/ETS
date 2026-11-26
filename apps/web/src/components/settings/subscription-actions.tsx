"use client";

import { useSubscriptionActions } from "@/hooks/use-subscription-actions";
import type { SubscriptionDetailsProps } from "@/types/billing";

export function SubscriptionActions({ status }: SubscriptionDetailsProps) {
  const { busy, error, manageUrl, cancel } = useSubscriptionActions(status.can_manage);

  return (
    <div>
      {status.can_manage && (
        manageUrl ? (
          <a href={manageUrl} target="_blank" rel="noopener noreferrer">
            Manage billing
          </a>
        ) : (
          !error && <span role="status">Loading billing link...</span>
        )
      )}{" "}
      {status.can_cancel && (
        <button type="button" onClick={cancel} disabled={busy}>
          Cancel subscription
        </button>
      )}
      {error && <p role="alert">{error}</p>}
    </div>
  );
}