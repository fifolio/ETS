"use client";

import { useRouter } from "next/navigation";

import { usePlans } from "@/hooks/use-plans";
import { useSubscriptionStatus } from "@/hooks/use-subscription-status";
import { readSubscription } from "@/lib/account/read-subscription";
import { useAuthStore } from "@/stores/auth/auth-store";

import { PlanList } from "./plan-list";
import { SubscriptionDetails } from "./subscription-details";

export function SubscriptionSection() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const { plans, paymentsEnabled, error, loaded } = usePlans();
  const { data: status, error: statusError } = useSubscriptionStatus();

  if (!user) {
    return null;
  }
  const currentPlan = status?.plan ?? readSubscription(user);
  const currentName = plans.find((plan) => plan.id === currentPlan)?.name ?? currentPlan;

  return (
    <section>
      <h2>Subscription</h2>
      <p>Your plan: {currentName}</p>
      {status && <SubscriptionDetails status={status} />}
      {statusError && <p role="alert">{statusError}</p>}
      {error && <p role="alert">{error}</p>}
      {!loaded && !error && <p>Loading...</p>}
      {loaded && (
        <PlanList
          plans={plans}
          currentPlan={currentPlan}
          paymentsEnabled={paymentsEnabled}
          busy={false}
          onUpgrade={(plan) => router.push(`/subscribe?product=${plan}`)}
        />
      )}
    </section>
  );
}