import { describeRenewal } from "@/lib/billing/describe-renewal";
import type { SubscriptionDetailsProps } from "@/types/billing";

import { SubscriptionActions } from "./subscription-actions";

export function SubscriptionDetails({ status }: SubscriptionDetailsProps) {
  return (
    <div>
      <p>{describeRenewal(status)}</p>
      {(status.can_manage || status.can_cancel) && <SubscriptionActions status={status} />}
    </div>
  );
}