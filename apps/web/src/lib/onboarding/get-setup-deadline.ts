import { SETUP_DEADLINE_HOURS } from "@/constants/account-defaults";

export function getSetupDeadline(createdAt: string): Date {
    return new Date(new Date(createdAt).getTime() + SETUP_DEADLINE_HOURS * 60 * 60 * 1000);
}