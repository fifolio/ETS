import { describeCredits } from "@/lib/plans/describe-credits";
import { describeJobBoards } from "@/lib/plans/describe-job-boards";
import { formatPlanPrice } from "@/lib/plans/format-plan-price";
import type { PlanCardProps } from "@/types/plans";
import { TimeSavedLine } from "../billing/time-saved-line";

export function PlanCard({
  plan,
  current,
  upgradable,
  paymentsEnabled,
  busy,
  onUpgrade,
}: PlanCardProps) {
  return (
    <li>
      <strong>{plan.name}</strong>
      {current && " (your plan)"}
      <br />
      {describeJobBoards(plan.job_board_count)},{" "}
      {formatPlanPrice(plan.price_usd_per_month)}
      {upgradable && (
        <>
          <br />
          <button
            type="button"
            onClick={() => onUpgrade(plan.id)}
            disabled={!paymentsEnabled || busy}
          >
            {paymentsEnabled ? `Upgrade to ${plan.name}` : "Upgrades open soon"}
          </button>
        </>
      )}
      <br />
      {describeCredits(plan.monthly_credits)}
      <br />
      <TimeSavedLine credits={plan.monthly_credits} perMonth />
    </li>
  );
}
