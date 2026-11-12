import { describeJobBoards } from "@/lib/plans/describe-job-boards";
import { formatPlanPrice } from "@/lib/plans/format-plan-price";
import type { PlanCardProps } from "@/types/plans";

export function PlanCard({ plan, current, upgradable, paymentsEnabled, busy, onUpgrade }: PlanCardProps) {
    return (
        <li>
            <strong>{plan.name}</strong>
            {current && " (your plan)"}
            <br />
            {describeJobBoards(plan.max_job_boards)}, {formatPlanPrice(plan.price_usd_per_month)}
            {upgradable && (
                <>
                    <br />
                    <button type="button" onClick={() => onUpgrade(plan.id)} disabled={!paymentsEnabled || busy}>
                        {paymentsEnabled ? `Upgrade to ${plan.name}` : "Upgrades open soon"}
                    </button>
                </>
            )}
        </li>
    );
}